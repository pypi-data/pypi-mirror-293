__all__ = [
    "torch",
    "th",
    "torchvision",
    "T",
    "transforms",
    "nn",
    "np",
    "F",
    "Dataset",
    "DataLoader",
    "optim",
    "Report",
    "Reshape",
    "Permute",
    "device",
    "save_torch_model_weights_from",
    "load_torch_model_weights_to",
    "detach",
    "cat_with_padding",
]

import time
import torch
import matplotlib.pyplot as plt
from collections import defaultdict, namedtuple
from typing import List, Union
import numpy as np
from itertools import dropwhile, takewhile
from loguru import logger

# Python第三方库，用于在命令行界面或Jupyter笔记本中显示进度条。它可以帮助用户在长时间运行的任务中获得更好的用户体验
from tqdm import trange


device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    import wandb
except ImportError:
    pass

try:
    from mlflow_extend import mlflow
except ImportError:
    mlflow = None

metric = namedtuple("metric", "pos,val".split(","))


class Report:
    def __init__(
        self,
        n_epochs=None,
        precision=3,
        old_report=None,
        wandb_project=None,
        hyper_parameters=None,
        **kwargs,
    ) -> None:
        self.start = time.time()
        self.n_epochs = n_epochs
        self.precision = precision
        self.completed_epochs = -1
        self.logged = set()
        self.set_external_logging(wandb_project, hyper_parameters)

    def reset_time(self):
        self.start = time.time()

    def prepend(self, old_report):
        for k in old_report.logged:
            self.logged.add(k)
            last = getattr(old_report, k)[-1].pos
            setattr(self, k, [])
            for m in getattr(old_report, k):
                getattr(self, k).append(metric(m.pos - last, to_np(m.val)))

    def record(self, pos, **metrics):
        metrics = {k: to_np(v) for k, v in metrics.items()}
        for k, v in metrics.items():
            if k in ["end", "pos"]:
                continue
            if hasattr(self, k):
                getattr(self, k).append(metric(pos, to_np(v)))
            else:
                setattr(self, k, [])
                getattr(self, k).append(metric(pos, to_np(v)))
                self.logged.add(k)

        if not any(["val" in key for key in metrics.keys()]):
            key = "train_step"
            step = self.train_step
        else:
            key = "validation_step"
            step = self.validation_step

        self.report_metrics(pos, **metrics)

        metrics = {k: v for k, v in metrics.items() if not isinstance(v, str)}
        if self.wandb_logging:
            wandb.log({**metrics, key: step})
        if self.mlflow_logging:
            mlflow.log_metrics(metrics, step=step)

        if key == "train_step":
            self.train_step += 1
        else:
            self.validation_step += 1

    def plot(self, keys: Union[List, str] = None, smooth=0, ax=None, **kwargs):
        _show = True if ax is None else False
        if ax is None:
            sz = 8, 6
            fig, ax = plt.subplots(figsize=kwargs.get("figsize", sz))

        keys = self.logged if keys is None else keys
        if isinstance(keys, str):
            key_pattern = keys
            keys = [key for key in self.logged if re.search(key_pattern, key)]

        for k in keys:
            xs, ys = list(zip(*getattr(self, k)))
            if smooth:
                ys = moving_average(np.array(ys), smooth)

            if "val" in k:
                _type = "--"
            elif "test" in k:
                _type = ":"
            else:
                _type = "-"

            ax.plot(xs, ys, _type, label=k)
        ax.grid(True)
        ax.set_xlabel("Epochs")
        ax.set_ylabel("Metrics")
        ax.set_title(
            kwargs.get("title", None), fontdict=kwargs.get("fontdict", {"size": 20})
        )
        if kwargs.get("log", False):
            ax.semilogy()
        ax.legend()
        if _show:
            plt.show()

    def history(self, k):
        return [v for _, v in getattr(self, k)]

    def plot_epochs(self, keys: list = None, ax=None, **kwargs):
        _show = True if ax is None else False
        if ax is None:
            sz = 8, 6
            fig, ax = plt.subplots(figsize=kwargs.get("figsize", sz))
        avgs = defaultdict(list)
        keys = self.logged if keys is None else keys

        if isinstance(keys, str):
            key_pattern = keys
            keys = [key for key in self.logged if re.search(key_pattern, key)]
        xs = []
        for epoch in trange(-100, self.n_epochs + 1):
            for k in keys:
                items = takewhile(
                    lambda x: epoch - 1 <= x.pos < epoch,
                    dropwhile(
                        lambda x: (epoch - 1 > x.pos or x.pos > epoch), getattr(self, k)
                    ),
                )
                items = list(items)
                if items == []:
                    continue
                xs.append(epoch)
                avgs[k].append(np.mean([v for pos, v in items]))
            xs = sorted(set(xs))

        for k in avgs:
            if "val" in k:
                _type = "--"
            elif "test" in k:
                _type = ":"
            else:
                _type = "-"
            if len(avgs[k]) != len(xs):
                logger.info(
                    f"metric {k} was not fully recorded. Plotting final epochs using last recorded value"
                )
                avgs[k].extend([avgs[k][-1]] * (len(xs) - len(avgs[k])))
            ax.plot(
                xs,
                avgs[k],
                _type,
                label=k,
            )
        ax.grid(True)
        ax.set_xlabel("Epochs")
        ax.set_ylabel("Metrics")
        ax.set_title(
            kwargs.get("title", None), fontdict=kwargs.get("fontdict", {"size": 20})
        )
        if kwargs.get("log", False):
            ax.semilogy()
        plt.legend()
        if _show:
            plt.show()

    def report_avgs(self, epoch, return_avgs=True, end="\n"):
        avgs = {}
        for k in self.logged:
            avgs[k] = np.mean(
                [v for pos, v in getattr(self, k) if epoch - 1 <= pos < epoch]
            )
        self.report_metrics(epoch, end=end, **avgs)
        avgs = {f"epoch_{k}": v for k, v in avgs.items()}
        if self.wandb_logging:
            wandb.log({**avgs, "epoch": epoch})
        if self.mlflow_logging:
            mlflow.log_metrics(avgs, step=epoch)
        if return_avgs:
            return avgs

    def report_metrics(self, pos, **report):
        """Report training and validation metrics
        Required variables to be initialized before calling this function:
        1. start (time.time())
        2. n_epochs (int)

        Special kwargs:
        1. end - line ending after print (default newline)
        2. log - prefix info before printing summary

        Special argument:
        1. pos - position in training/testing process - float between 0 - n_epochs

        Usage:
        report_metrics(pos=1.42, train_loss=train_loss, validation_loss=validation_loss, ... )
        where each kwarg is a float
        """
        elapsed = time.time() - self.start
        end = report.pop("end", "\n")
        log = report.pop("log", "")
        log = log + ": " if log != "" else log
        elapsed = "  ({:.2f}s - {:.2f}s remaining)".format(
            time.time() - self.start, ((self.n_epochs - pos) / pos) * elapsed
        )
        current_iteration = f"EPOCH: {pos:.3f}  "
        if end == "\r":
            print(
                f"\r{log}{current_iteration}{info(report, self.precision)}{elapsed}",
                end="",
            )
        else:
            print(
                f"\r{log}{current_iteration}{info(report, self.precision)}{elapsed}",
                end=end,
            )

    def set_external_logging(self, project=None, hyper_parameters=None):
        if project is not None:
            if "/" in project:
                project, name = project.split("/")
            self.wandb_logging = True
            wandb.init(project=project, name=name, config=hyper_parameters)
        else:
            self.wandb_logging = False

        if mlflow and mlflow.active_run():
            self.mlflow_logging = True
        else:
            self.mlflow_logging = False

        self.train_step = 0
        self.validation_step = 0

    def finish_run(self, **kwargs):
        if not kwargs.get("do_not_finish_wandb", False):
            if self.wandb_logging:
                wandb.finish()


def to_np(x):
    if isinstance(x, torch.Tensor):
        return float(x.detach().cpu().numpy())
    else:
        return x


def moving_average(a, n=3):
    b = np.zeros_like(a)
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    _n = len(b) - n
    b[-_n - 1 :] = ret[(n - 1) :] / n
    return b
