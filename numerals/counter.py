class Counter:
    '''The Counter class is a collection of individual counters.  It is
    intended to count the occurences of numerals (integers), but it
    may also be used to count other things.

    '''

    # The minimal value to consider.
    _min_value = 0

    # The maximal value to consider.
    _max_value = 1

    # The actual dictionary of counters: value => counter.
    # If no key exists in this dictionary for a spefic value,
    # its counter is assumed to 0.
    _counters = {}

    def __init__(self, min=0, max=100):
        '''Create a new counter.

        Arguments
        ---------
        min : int
            The minimal value to count. All smaller values will be ignored.
        max : int
            The maximal value to count. All larger values will be ignored.
        '''
        self._max_value = max
        # [p] why is _min_value not adjusted to the input argument min?
        self.reset()


    def __call__(self, *arg):
        '''Count given value(s). The respective counter(s) is/are increased
        by 1.

        Arguments
        ---------
        arg: (ints) or [ints]
                Either an individual number value or a list or tuple
                of numbers. If a number occurs multiple times in the
                list/tuple, then the corresponding count will be increased
                once for each occurence.
        '''
        if len(arg) != 1:
            return self(arg)
        arg = arg[0]
        if isinstance(arg,(list,tuple)):
            list(map(self, arg))
        elif arg >= self._min_value and arg <= self._max_value:
            # not yet in dictionary: new entry
            if not arg in self._counters:
                self._counters[arg] = 1
            else:
                # already in dictionary: increase
                self._counters[arg] += 1


    def __getitem__(self, *arg):
        '''Access individual counter(s).

        Arguments:
        ---------
        *arg: (ints) or [ints]
                Either an individual number value or a list of numbers.

        Result
        ------
        int or [ints]
                Depending on the input argument, either a single counter
                value, or a list of counter values is returned.
                In the latter case, the order of counters values corresponds
                to the order of numbers in the argument list.
        '''
        if len(arg) != 1:
            return self.__getitem__(arg)
        arg = arg[0]
        if isinstance(arg,(list,tuple)):
            return list(map(self.__getitem__, arg))
        else:
            return self._counters[arg] if arg in self._counters else 0


    def sum(self):
        '''Get the sum of all element counters.

        Result
        ------
        The sum of all element counters.
        '''
        return sum(self._counters.values())


    def reset(self):
        '''Reset this counter object.
        This will just set all counters to 0 but will keep all
        other parameters.
        '''
        self._counters = {}
