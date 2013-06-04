def distribute_space(available, focus_idx, give, want=None):
    """
    Distribute available space to items, priority to focused item.

    Result list "give" is modified in-place. It should initially contain
    the minimum space required for each item.
    The optional list "want" should contain the space that each item wants
    to use additionally.
    """
    if not want:
        want = [0 for g in give]
    # not even enough space for focused item
    if available < give[focus_idx]:
        for i in range(len(give)):
            give[i] = 0 if i != focus_idx else available
    # not enough space for every item -> trim
    elif available < sum(give):
        over = sum(give) - available
        i = 0
        j = len(give)-1
        while True:
            if j > focus_idx:
                if give[j] >= over:
                    give[j] -= over
                    break
                else:
                    over -= give[j]
                    give[j] = 0
                    j -= 1
            if i < focus_idx:
                if give[i] >= over:
                    if focus_idx <= j < len(give)-1:
                        j += 1
                        give[j] += give[i]
                        over += give[i]
                over -= give[i]
                give[i] = 0
                i += 1
                if over <= 0:
                    break
    # enough space for every item -> give more to those who want
    else:
        i = 0
        while sum(give) < available and sum(want) > 0:
            if want[i] > 0:
                want[i] -= 1
                give[i] += 1
            i = (i+1)%len(give)
