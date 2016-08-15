class UpdateHeuristics:
    """
    Heuristics to control thread based updates with user
    triggered updates.
    """

    ticks = 0
    updated = 0

    @staticmethod
    def tick():
        UpdateHeuristics.ticks += 1
        UpdateHeuristics.updated += 1

    @staticmethod
    def force_unupdate():
        UpdateHeuristics.updated += 1

    @staticmethod
    def skip_update():
        diff_heuristic = UpdateHeuristics.updated - UpdateHeuristics.ticks

        if 2 < diff_heuristic < 10:
            UpdateHeuristics.updated = 0
            return True
        elif 30 > diff_heuristic > 2:
            UpdateHeuristics.updated -= 1
            return False

        UpdateHeuristics.updated = 0
        return False
