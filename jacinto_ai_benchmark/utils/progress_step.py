import sys
from colorama import Fore
from tqdm.auto import tqdm

__all__ = ['progress_step', 'progress_step2']


def progress_step(iterable, desc, desc_len=60, total=None, miniters=None, bar_format=None, file=sys.stdout,
                  leave=True, colors=(Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA), **kwargs):
    desc = desc[:desc_len] if (desc_len is not None and len(desc) > desc_len) else \
        desc + ' '*(desc_len-len(desc))
    if miniters is None:
        iter_length = len(iterable) if hasattr(iterable, '__len__') else total
        miniters = max(iter_length//100, 1) if iter_length is not None else 1
    #
    if bar_format is None:
        format_arg = (colors[0], desc_len, colors[1], colors[2], colors[3], Fore.RESET)
        bar_format = '%s{desc:%s}|%s{percentage:4.0f}%%|%s{bar:10}|%s{r_bar}%s' % format_arg
    #
    return TqdmStep(iterable=iterable, desc=desc, total=total, miniters=miniters, bar_format=bar_format, file=file,
                leave=leave, **kwargs)


class TqdmStep(tqdm):
    def __init__(self, iterable, *args, miniters=None, **kwargs):
        super().__init__(iterable, *args, miniters=miniters, **kwargs)
        assert 'miniters' is not None, 'miniters must be provided'
        self.step_size = miniters
        self.iter_index = 0
        self.steps_counted = 0

    def update(self, n=1):
        steps_counted = self.iter_index//self.step_size
        if steps_counted > self.steps_counted:
            for _ in range(self.steps_counted, steps_counted):
                super().update(self.step_size)
            #
            self.steps_counted = steps_counted
        elif hasattr(self, '__len__') and self.iter_index == (self.__len__()-1):
            super().update(self.iter_index % self.step_size)
        #
        self.iter_index += n


######################################################################
import time
from .timer_utils import display_timing_stats


# a lighter version of progress_step (uses different default colors)
# this prints the iteration descriptor before the iteration starts (not after it)
def progress_step2(iterable, desc, desc_len=60, colors=(Fore.BLUE, Fore.MAGENTA, Fore.YELLOW, Fore.CYAN), **kwargs):
    return ProgStep(iterable, desc, desc_len=desc_len, colors=colors, **kwargs)


class ProgStep:
    """
    a simple progress indicator that can be used instead of tqdm
    Author: Manu Mathew
    2021 Feb 16
    """
    def __init__(self, iterable, desc, desc_len=60, miniters=1, total=None, file=None, **kwargs):
        super().__init__()
        self.step_size = miniters
        self.iterable = iterable
        self.desc = desc[:desc_len] if (desc_len is not None and len(desc) > desc_len) else \
            desc + ' '*(desc_len-len(desc))
        self.total = iterable.__len__() if hasattr(iterable, '__len__') else total
        self.file = file if file is not None else sys.stdout
        self.num_completed = 0

    def __iter__(self):
        start_time = time.time()
        for item_id, item in enumerate(self.iterable):
            end_time = time.time()
            display_timing_stats(self.desc, self.num_completed, total=self.total,
                                 start_time=start_time, end_time=end_time,
                                 file=self.file)
            yield item
            self.num_completed = item_id + 1
            # only at the last iteration, print the final stat
            if self.num_completed == self.total:
                display_timing_stats(self.desc, self.num_completed, total=self.total,
                     start_time=start_time, end_time=end_time,
                     file=self.file)
            #
