# pylint: disable=too-many-branches
# pylint: disable=too-many-nested-blocks
from collections import abc
import time
import math
import typing
import torch
from auto_mind.supervised._action_data import (
    TestResult, TrainResult, ExecutionCursor, EarlyStopper, StateWithMetrics,
    TrainEarlyStopper, TrainEpochInfo, TrainBatchInfo, TrainParams, EvalParams,
    TestParams)
from auto_mind.supervised._action_handlers import (
    BatchExecutor, BatchAccuracyCalculator, MetricsCalculator, MetricsCalculatorInputParams,
    MetricsCalculatorParams, AbortedException)
from auto_mind.supervised._state_handler import StateHandler
from auto_mind.supervised._batch_handler import (
    MetricsHandler, TrainBatchHandler, TestBatchHandler)
from auto_mind.supervised._base_runner import BaseRunner, BaseRunnerParams

I = typing.TypeVar("I", bound=abc.Sized)
O = typing.TypeVar("O")
TG = typing.TypeVar("TG", bound=abc.Sized)
MT = typing.TypeVar("MT")

####################################################
################## General Action ##################
####################################################

class GeneralAction(typing.Generic[I, O, TG, MT]):
    """
    A class to represent a general action in a supervised learning context.

    This class encapsulates the logic for performing actions such as training,
    evaluation, and prediction in a supervised learning workflow. It handles
    the execution of these actions and manages the associated states and results.

    Methods:
        train(params: TrainParams) -> TrainResult | None:
            Trains the model using the provided parameters.
        test(params: TestParams) -> TestResult | None:
            Tests the model using the provided parameters.
        load_eval_state(params: EvalParams) -> None:
            Loads the evaluation state using the provided parameters.
        info(save_path: str) -> StateWithMetrics | None:
            Returns the state with metrics for the provided save path.
        define_as_pending(save_path: str) -> None:
            Defines the training state as pending for the provided save path.
        define_as_completed(save_path: str) -> None:
            Defines the training state as completed for the provided save path.
    """
    def __init__(
        self,
        random_seed: int | None,
        use_best: bool,
        executor: BatchExecutor[I, O],
        accuracy_calculator: BatchAccuracyCalculator[I, O, TG] | None,
        metrics_handler: MetricsHandler[I, O, TG, MT] | None,
        metrics_calculator: MetricsCalculator | None = None,
    ):
        main_state_handler = StateHandler[
            TrainParams[I, O, TG, MT],
            TestParams[I, O, TG, MT],
        ](use_best=use_best)

        base_runner = BaseRunner(
            random_seed=random_seed,
            executor=executor,
            accuracy_calculator=accuracy_calculator,
            metrics_handler=metrics_handler,
        )

        self._state_handler = main_state_handler
        self._metrics_handler = metrics_handler
        self._metrics_calculator = metrics_calculator
        self._base_runner = base_runner

    def load_eval_state(self, params: EvalParams) -> None:
        self._state_handler.load_eval_state(params)

    def info(self, save_path: str) -> StateWithMetrics | None:
        return self._state_handler.info(save_path=save_path)

    def define_as_pending(self, save_path: str) -> None:
        self._state_handler.define_as_completed(completed=False, save_path=save_path)

    def define_as_completed(self, save_path: str) -> None:
        self._state_handler.define_as_completed(completed=True, save_path=save_path)

    def _can_run(self, early_stopper: EarlyStopper | None) -> bool:
        if not early_stopper:
            return True

        return not early_stopper.check()

    def calculate_metrics(
        self,
        params: MetricsCalculatorInputParams,
    ) -> dict[str, typing.Any] | None:
        state_handler = self._state_handler
        metrics_calculator = self._metrics_calculator
        save_path = params.save_path

        if not metrics_calculator or not save_path:
            return None

        info = state_handler.load_state_with_metrics(save_path=save_path)

        if not info:
            return None

        calc_params = MetricsCalculatorParams(info=info, model=params.model)
        metrics = metrics_calculator.run(calc_params)

        state_handler.save_metrics(metrics, save_path=save_path)

        return metrics

    def train(self, params: TrainParams[I, O, TG, MT]) -> TrainResult | None:
        full_state, _ = self._state_handler.load_train_state(params)
        results: TrainResult | None = full_state.train_results if full_state else None

        try:
            if (not results) or (not results.early_stopped):
                return self._train(params)

            return results
        except AbortedException:
            return None

    def test(self, params: TestParams[I, O, TG, MT]) -> TestResult | None:
        try:
            return self._test(params)
        except AbortedException:
            return None

    def _train(self, params: TrainParams[I, O, TG, MT]) -> TrainResult:
        epochs = params.epochs
        batch_interval = params.batch_interval
        save_every = params.save_every
        print_every = params.print_every
        metric_every = params.metric_every
        early_stopper = params.early_stopper
        get_epoch_info = params.get_epoch_info or default_epoch_info
        train_dataloader = params.train_dataloader
        validation_dataloader = params.validation_dataloader
        validate = validation_dataloader is not None

        full_state, state_dict = self._state_handler.load_train_state(params)
        results: TrainResult = (
            full_state.train_results
            if full_state
            else TrainResult.initial_state(
                validate=validate,
                has_metrics_handler=self._metrics_handler is not None,
            ))
        start_epoch = results.epoch + 1

        print_count = 0
        print_loss: float = 0
        print_accuracy: float | None = 0
        print_val_loss: float = 0
        print_val_accuracy : float | None= 0

        # Keep track of losses and accuracies for the metrics
        metric_count = 0
        metric_loss: float = 0
        metric_accuracy: float | None = 0
        metric_train_time = 0
        metric_val_loss: float = 0
        metric_val_accuracy: float | None = 0
        metric_val_time = 0

        print_metrics: typing.Any | None = None
        print_val_metrics: typing.Any | None = None
        metrics: typing.Any | None = None

        epoch = 0
        train_loss: float = 0.0
        train_accuracy: float | None = 0.0
        val_loss: float = 0.0
        val_accuracy: float | None = 0.0
        train_metrics: typing.Any | None = None
        val_metrics: typing.Any | None = None

        get_batch_info = params.get_batch_info if params.get_batch_info else default_batch_info
        metrics_handler = self._metrics_handler

        def update_results() -> None:
            results.epoch = epoch
            results.train_batch = 0
            results.val_batch = 0
            results.batch_train_cursor = None
            results.batch_val_cursor = None
            results.epoch_cursor = ExecutionCursor(
                amount=metric_count,
                total_loss=metric_loss,
                total_accuracy=metric_accuracy,
                total_time=metric_train_time,
                total_metrics=metrics)
            results.last_train_loss = train_loss
            results.last_train_accuracy = train_accuracy
            results.last_train_metrics = train_metrics
            results.last_val_loss = val_loss
            results.last_val_accuracy = val_accuracy
            results.last_val_metrics = val_metrics

            if not validate:
                results.last_loss = train_loss
                results.last_accuracy = train_accuracy
                results.last_metrics = train_metrics
            else:
                results.last_loss = val_loss
                results.last_accuracy = val_accuracy
                results.last_metrics = val_metrics

        start = time.time()

        if print_every is not None:
            if start_epoch < epochs + 1:
                print_str = f'Starting training for {epochs} epochs...'
                max_len = len(print_str)

                if start_epoch > 1:
                    next_print_str = f'(starting from epoch {start_epoch})'
                    print_str += f'\n{next_print_str}'
                    max_len = max(max_len, len(next_print_str))

                separator = '=' * max_len
                print(print_str)
                print(separator)
            else:
                print(f'Training already completed ({epochs} epochs).')

        def verify_early_stop(new_iteration: bool) -> TrainResult | None:
            nonlocal epoch
            early_stopper = params.early_stopper

            if early_stopper:
                stopped = early_stopper.check()
                finished = isinstance(
                    early_stopper,
                    TrainEarlyStopper,
                ) and early_stopper.check_finish()

                if finished or stopped:
                    save_result = (
                        (finished and (not results.early_stopped))
                        or
                        (
                            new_iteration
                            and
                            stopped
                            and
                            (epoch > start_epoch)
                            and
                            (epoch > results.epoch)
                        )
                    )

                    if save_result:
                        epoch = (epoch - 1) if new_iteration else epoch
                        update_results()

                        if finished:
                            results.early_stopped = True

                        self._state_handler.save_train_state(
                            params,
                            results,
                            state_dict)

                    if finished:
                        return results

                    raise AbortedException()

            return None

        try:
            for epoch in range(start_epoch, epochs + 1):
                r = verify_early_stop(new_iteration=True)
                if r:
                    return r

                batch_handler = TrainBatchHandler(
                    validation=False,
                    epoch=epoch,
                    params=params,
                    results=results,
                    save_state=lambda result: self._state_handler.save_train_state(
                        params, result, state_dict),
                    early_stopper=early_stopper,
                    metrics_handler=metrics_handler,
                    get_batch_info=get_batch_info)

                with torch.set_grad_enabled(True):
                    result = self._base_runner.run(BaseRunnerParams(
                        epoch=epoch,
                        is_train=True,
                        dataloader=train_dataloader,
                        model=params.model,
                        criterion=params.criterion,
                        optimizer=params.optimizer,
                        scheduler=params.scheduler if not validate else None,
                        clip_grad_max=params.clip_grad_max,
                        hook=params.train_hook,
                        step_only_on_accuracy_loss=params.step_only_on_accuracy_loss,
                        batch_handler=batch_handler,
                    ))

                train_loss = result.total_loss
                train_accuracy = result.total_accuracy
                train_time = result.total_time
                train_metrics = result.total_metrics

                metric_loss += train_loss
                print_loss += train_loss
                if metric_accuracy is not None and train_accuracy is not None:
                    metric_accuracy += train_accuracy
                else:
                    metric_accuracy = None
                if print_accuracy is not None and train_accuracy is not None:
                    print_accuracy += train_accuracy
                else:
                    print_accuracy = None
                metric_train_time += train_time

                if train_metrics:
                    print_metrics = metrics_handler.add(
                        print_metrics,
                        train_metrics,
                    ) if metrics_handler else None
                    metrics = metrics_handler.add(
                        metrics,
                        train_metrics,
                    ) if metrics_handler else None

                val_result = None

                if not validate:
                    if params.early_stopper and isinstance(params.early_stopper, TrainEarlyStopper):
                        params.early_stopper.update_epoch(
                            loss=train_loss,
                            accuracy=train_accuracy,
                            metrics=train_metrics)
                else:
                    batch_handler = TrainBatchHandler(
                        validation=True,
                        epoch=epoch,
                        params=params,
                        results=results,
                        save_state=lambda result: self._state_handler.save_train_state(
                            params, result, state_dict),
                        early_stopper=early_stopper,
                        metrics_handler=metrics_handler,
                        get_batch_info=get_batch_info)

                    with torch.set_grad_enabled(False):
                        assert validation_dataloader is not None
                        val_result = self._base_runner.run(BaseRunnerParams(
                            epoch=epoch,
                            is_train=False,
                            dataloader=validation_dataloader,
                            model=params.model,
                            criterion=params.criterion,
                            optimizer=None,
                            scheduler=params.scheduler,
                            clip_grad_max=None,
                            hook=params.validation_hook,
                            step_only_on_accuracy_loss=params.step_only_on_accuracy_loss,
                            batch_handler=batch_handler,
                        ))

                    if val_result:
                        val_loss = val_result.total_loss
                        val_accuracy = val_result.total_accuracy
                        val_time = val_result.total_time
                        val_metrics_item = val_result.total_metrics

                        metric_val_loss += val_loss
                        print_val_loss += val_loss
                        if val_accuracy is not None:
                            if metric_val_accuracy is not None:
                                metric_val_accuracy += val_accuracy

                            if print_val_accuracy is not None:
                                print_val_accuracy += val_accuracy
                        else:
                            metric_val_accuracy = None
                            print_val_accuracy = None
                        metric_val_time += val_time

                        if val_metrics_item:
                            print_val_metrics = metrics_handler.add(
                                print_val_metrics,
                                val_metrics_item,
                            ) if metrics_handler else None
                            val_metrics = metrics_handler.add(
                                val_metrics,
                                val_metrics_item,
                            ) if metrics_handler else None

                        if params.early_stopper and isinstance(
                            params.early_stopper,
                            TrainEarlyStopper,
                        ):
                            params.early_stopper.update_epoch(
                                loss=val_loss,
                                accuracy=val_accuracy,
                                metrics=val_metrics_item)

                print_count += 1
                metric_count += 1
                last = epoch == epochs

                # print every print_every epochs, or if last epoch,
                # or if batch_interval is set (to print partial epochs)
                do_print = (
                    (print_every is not None)
                    and
                    (batch_interval or last or (epoch % print_every == 0))
                )
                # save every save_every epochs, or if last epoch,
                # or if batch_interval is set (to save partial epochs)
                do_save = (
                    (save_every is not None)
                    and
                    (batch_interval or last or (epoch % save_every == 0))
                )
                # update changes the result to store, which is done when going to save,
                # and also when defining the metrics
                do_update = do_save or last or (metric_every is None) or (epoch % metric_every == 0)
                # change metric values when updating, as long as metric_every is set
                do_metric = do_update and (metric_every is not None)

                if do_print:
                    info: TrainEpochInfo[typing.Any] = TrainEpochInfo(
                        epochs=epochs,
                        epoch=epoch,
                        start_epoch=start_epoch,
                        start=start,
                        loss=print_loss,
                        val_loss=print_val_loss,
                        accuracy=print_accuracy,
                        val_accuracy=print_val_accuracy,
                        metrics=print_metrics,
                        val_metrics=print_val_metrics,
                        count=print_count,
                        validate=bool(val_result),
                        batch_interval=batch_interval)
                    get_epoch_info = (
                        params.get_epoch_info
                        if params.get_epoch_info else
                        default_epoch_info)
                    print_info = get_epoch_info(info)

                    if print_info:
                        print(print_info)

                    print_count = 0
                    print_loss = 0
                    print_accuracy = 0
                    print_val_loss = 0
                    print_val_accuracy = 0
                    print_metrics = None

                if do_update:
                    update_results()

                    if not do_metric:
                        results.total_train_time += metric_train_time
                        results.total_val_time += metric_val_time
                        metric_train_time = 0
                        metric_val_time = 0
                    else:
                        results.total_train_time += metric_train_time
                        results.total_val_time += metric_val_time

                        if metric_accuracy is not None:
                            results.accuracies.append(
                                (epoch, metric_accuracy / metric_count))
                        results.losses.append((epoch, metric_loss / metric_count))
                        results.times.append((epoch, metric_train_time))

                        if results.metrics is not None:
                            results.metrics.append((epoch, metrics))

                        if val_result:
                            if results.val_accuracies is not None:
                                if metric_val_accuracy is not None:
                                    results.val_accuracies.append(
                                        (epoch, metric_val_accuracy / metric_count))

                            if results.val_losses is not None:
                                results.val_losses.append(
                                    (epoch, metric_val_loss / metric_count))

                            if results.val_times is not None:
                                results.val_times.append((epoch, metric_val_time))

                            if results.val_metrics is not None:
                                results.val_metrics.append((epoch, val_metrics))

                        # sort by accuracy, get the last one (best case)
                        accuracies_to_use = (
                            results.val_accuracies
                            if val_result and results.val_accuracies
                            else results.accuracies)
                        best_cases = sorted(accuracies_to_use, key=lambda x: x[1])
                        best_case = best_cases[-1] if best_cases else None

                        if best_case is not None and results.best_accuracy is not None:
                            best_epoch, best_accuracy = best_case

                            if best_accuracy > results.best_accuracy:
                                results.best_epoch = best_epoch
                                results.best_accuracy = best_accuracy

                        metric_count = 0
                        metric_loss = 0
                        metric_accuracy = 0
                        metric_train_time = 0
                        metric_val_loss = 0
                        metric_val_accuracy = 0
                        metric_val_time = 0
                        metrics = None
                        val_metrics = None

                    if do_save:
                        self._state_handler.save_train_state(
                            params,
                            results,
                            state_dict)
        except AbortedException as e:
            r = verify_early_stop(new_iteration=False)
            if r:
                return r
            raise e

        return results

    def _test(self, params: TestParams[I, O, TG, MT]) -> TestResult:
        test_state, state_dict = self._state_handler.load_test_state(params)
        train_results = test_state.train_results if test_state else None
        epoch = (train_results.epoch or 0) if train_results else 0
        test_results: TestResult | None = test_state.test_results if test_state else None
        test_epoch = test_results.epoch if test_results else None

        early_stopper = params.early_stopper
        metrics_handler = self._metrics_handler

        get_batch_info = params.get_batch_info if params.get_batch_info else default_batch_info

        test_dataloader = params.dataloader
        assert test_dataloader is not None, 'the test dataloader is empty'

        if not self._can_run(early_stopper):
            raise AbortedException()

        if (
            (not test_results)
            or
            test_results.batch
            or
            (test_epoch is None)
            or
            (test_epoch < epoch)
        ):
            print_str = 'Starting test...'
            separator = '=' * len(print_str)
            print(separator)
            print(print_str)

            test_results = TestResult(
                epoch=epoch,
                loss=0.0,
                accuracy=0.0,
                total_time=0,
                batch=0,
                total_batch=None,
                last_epoch_losses=None,
                last_epoch_accuracies=None,
                last_epoch_times=None)

            batch_handler = TestBatchHandler(
                params=params,
                results=test_results,
                save_state=lambda result: self._state_handler.save_test_state(
                    params, result, state_dict),
                early_stopper=early_stopper,
                metrics_handler=metrics_handler,
                get_batch_info=get_batch_info)

            with torch.set_grad_enabled(False):
                result = self._base_runner.run(BaseRunnerParams(
                    epoch=epoch,
                    is_train=False,
                    dataloader=test_dataloader,
                    model=params.model,
                    criterion=params.criterion,
                    optimizer=None,
                    scheduler=None,
                    clip_grad_max=None,
                    hook=params.hook,
                    step_only_on_accuracy_loss=False,
                    batch_handler=batch_handler,
                ))

            if result:
                loss = result.total_loss
                accuracy = result.total_accuracy
                total_time = result.total_time

                test_results.epoch = epoch
                test_results.batch = 0
                test_results.loss = loss
                test_results.accuracy = accuracy
                test_results.total_time = total_time

                print_str = f'Test completed in {total_time/1000:.3f} seconds.'
                separator = '=' * len(print_str)
                print(separator)
                print(print_str)
                print(separator)
        else:
            if params.print_every is not None:
                print_str = f'test epoch: {test_epoch}, last trained epoch: {epoch}'
                print_str = f'Test already completed ({print_str}).'
                print(print_str)

        if not test_results:
            raise Exception('the test returned no result')

        if test_state and test_results:
            self._state_handler.save_test_state(
                params, test_results, state_dict)

        return test_results

####################################################
################ Private Functions #################
####################################################

def _as_minutes(s: float, spaces: int | None = None) -> str:
    m = math.floor(s / 60)
    s -= m * 60
    info = f'{m:.0f}m {s:02.2f}s'
    return f'{info:>{spaces}}' if spaces else info

def _time_since(since: float, percent: float, spaces: int | None = None) -> str:
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    passed = _as_minutes(s, spaces=spaces)
    remaining = _as_minutes(rs, spaces=spaces)
    return f'{passed} (eta: {remaining})'

####################################################
################# Public Functions #################
####################################################

def default_batch_info(info: TrainBatchInfo[typing.Any]) -> str:
    print_loss = info.loss or 0
    print_accuracy = info.accuracy
    print_count = info.count or 1
    batch = info.batch or 0
    total_batch = info.total_batch
    first = info.first
    last = info.last
    start = info.start or time.time()
    print_prefix = info.prefix or ''
    validation = info.validation
    test = info.test

    loss_avg = f'{(print_loss / print_count):.4f}'
    loss_avg = f'[loss: {loss_avg}]'

    if print_accuracy is not None:
        acc_str = f'{100.0 * print_accuracy / print_count:>5.1f}%'
        acc_str = f'[accuracy: {acc_str}]'
    else:
        acc_str = ''

    batch_cap = 10 if total_batch is None else math.ceil(math.log10(total_batch))
    batch_main_str = f'{batch:>{batch_cap}}'
    batch_str = f'[batch: {batch_main_str}]' if total_batch is None else (
        f'[batch: {batch_main_str}/{total_batch}]')
    now = time.time()
    diff_time = now - start
    time_str = _as_minutes(diff_time, spaces=11)
    time_str = f'[time: {time_str}]'

    result = f'{print_prefix}{batch_str} {time_str} {acc_str} {loss_avg}'

    if (first and validation) or (last and test):
        result_len = len(result)
        separator = ('=' if test else '-') * result_len
        result = f'{separator}\n{result}' if first else f'{result}\n{separator}'

    return result

def default_epoch_info(info: TrainEpochInfo[typing.Any]) -> str:
    epochs = info.epochs or 0
    epoch = info.epoch or 0
    start_epoch = info.start_epoch or 0
    start = info.start or time.time()
    loss = info.loss or 0
    val_loss = info.val_loss or 0
    accuracy = info.accuracy
    val_accuracy = info.val_accuracy
    count = info.count or 1
    validate = info.validate
    batch_interval = info.batch_interval

    train_loss_avg = loss / count
    val_loss_avg = val_loss / count
    loss_avg = (
        f'[val_loss: {val_loss_avg:.4f}, train_loss: {train_loss_avg:.4f}]'
        if validate
        else f'[loss: {train_loss_avg:.4f}]')

    train_acc_str = f'{100.0 * accuracy / count:>5.1f}%' if accuracy is not None else ''
    val_acc_str = (
        f'{100.0 * val_accuracy / count:>5.1f}%'
        if validate and (val_accuracy is not None)
        else '')

    if train_acc_str or val_acc_str:
        acc_str = (
            f'[val_accuracy: {val_acc_str}, train_accuracy: {train_acc_str}]'
            if train_acc_str and val_acc_str
            else (
                f'[accuracy: {train_acc_str}]'
                if train_acc_str
                else f'[val_accuracy: {val_acc_str}]'
            )
        )
    else:
        acc_str = ''

    epoch_cap = math.ceil(math.log10(epochs))
    epoch_str = f'[end of epoch {epoch:>{epoch_cap}} ({(100.0 * epoch / epochs):>5.1f}%)]'
    time_str = _time_since(start, (epoch - start_epoch + 1) / (epochs - start_epoch + 1), spaces=11)
    time_str = f'[time: {time_str}]'
    result = f'{epoch_str} {time_str} {acc_str} {loss_avg}'

    if batch_interval:
        result_len = len(result)
        separator_b = '-' * result_len
        separator_e = '=' * result_len
        result = f'{separator_b}\n{result}\n{separator_e}'

    return result
