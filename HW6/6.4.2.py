import math


class Segment:
    def __init__(self, start=None, end=None, include_start=False, include_end=False, is_empty=False):
        if isinstance(start, Segment):
            self.start = start.start
            self.end = start.end
            self.include_start = start.include_start
            self.include_end = start.include_end
            self.is_empty = start.is_empty
            return

        self.is_empty = is_empty
        if start is not None and end is not None:
            if start > end or (start == end and not (include_start and include_end)):
                self.is_empty = True

        if self.is_empty:
            self.start = float('inf')
            self.end = float('-inf')
            self.include_start = False
            self.include_end = False
        else:
            self.start = float(start)
            self.end = float(end)
            self.include_start = include_start
            self.include_end = include_end

    def contains(self, point):
        if self.is_empty:
            return False
        if point < self.start or point > self.end:
            return False
        if point == self.start and not self.include_start:
            return False
        if point == self.end and not self.include_end:
            return False
        return True

    def __str__(self):
        if self.is_empty:
            return "∅"
        left = "[" if self.include_start else "("
        right = "]" if self.include_end else ")"
        s_str = "-∞" if self.start == float('-inf') else f"{self.start:.2f}"
        e_str = "+∞" if self.end == float('inf') else f"{self.end:.2f}"
        return f"{left}{s_str}; {e_str}{right}"


class SegmentSetIterator:

    def __init__(self, segments):
        valid_segments = [s for s in segments if not s.is_empty]
        self._ordered = sorted(valid_segments, key=lambda x: x.start)
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._ordered):
            res = self._ordered[self._index]
            self._index += 1
            return res
        raise StopIteration


class SegmentSet:
    def __init__(self, initial=None):
        self.segments = []
        if isinstance(initial, SegmentSet):
            self.segments = [Segment(s) for s in initial.segments]
        elif isinstance(initial, Segment):
            self.segments = [initial]
        elif isinstance(initial, list):
            self.segments = initial

    def __iter__(self):
        return SegmentSetIterator(self.segments)

    def __str__(self):
        parts = [str(seg) for seg in self]
        return " ∪ ".join(parts) if parts else "∅"

    def __mul__(self, other):
        result_segments = []
        for s1 in self.segments:
            for s2 in other.segments:
                if s1.is_empty or s2.is_empty:
                    continue
                new_start = max(s1.start, s2.start)
                new_end = min(s1.end, s2.end)
                inc_start = s1.contains(new_start) and s2.contains(new_start)
                inc_end = s1.contains(new_end) and s2.contains(new_end)
                overlap = Segment(new_start, new_end, inc_start, inc_end)
                if not overlap.is_empty:
                    result_segments.append(overlap)

        return SegmentSet(result_segments)


def solve_inequality(a, b, c, strict):
    inc = not strict
    if a == 0:
        if b == 0:
            cond = c > 0 if strict else c >= 0
            return SegmentSet(Segment(float('-inf'), float('inf'))) if cond else SegmentSet()
        root = -c / b
        if b > 0:
            return SegmentSet(Segment(root, float('inf'), inc, False))
        else:
            return SegmentSet(Segment(float('-inf'), root, False, inc))

    d = b ** 2 - 4 * a * c

    if a > 0:
        if d < 0:
            return SegmentSet(Segment(float('-inf'), float('inf')))
        elif d == 0:
            root = -b / (2 * a)
            if inc:
                return SegmentSet(Segment(float('-inf'), float('inf')))
            else:
                return SegmentSet(
                    [Segment(float('-inf'), root, False, False), Segment(root, float('inf'), False, False)])
        else:
            r1 = (-b - math.sqrt(d)) / (2 * a)
            r2 = (-b + math.sqrt(d)) / (2 * a)
            return SegmentSet([Segment(float('-inf'), r1, False, inc), Segment(r2, float('inf'), inc, False)])

    else:  # a < 0, Парабола гілками вниз
        if d < 0:
            return SegmentSet()
        elif d == 0:
            root = -b / (2 * a)
            return SegmentSet(Segment(root, root, True, True)) if inc else SegmentSet()
        else:
            r1 = (-b + math.sqrt(d)) / (2 * a)
            r2 = (-b - math.sqrt(d)) / (2 * a)
            return SegmentSet(Segment(min(r1, r2), max(r1, r2), inc, inc))


if __name__ == "__main__":
    inequalities = [
        (1, 0, -4, False),
        (-1, 5, -4, True)
    ]


    solution_set = SegmentSet(Segment(float('-inf'), float('inf')))

    print("--- Процес розв'язання нерівностей ---")
    for a, b, c, strict in inequalities:
        single_solution = solve_inequality(a, b, c, strict)
        print(f"Нерівність ({a}x² + {b}x + {c} {'' if strict else '='}> 0) має розв'язок: {single_solution}")
        solution_set = solution_set * single_solution

    print("\n" + "=" * 40)
    print("ФІНАЛЬНА ВІДПОВІДЬ СИСТЕМИ:")
    print(solution_set)
    print("=" * 40)

    print("\nПеребір через ітератор:")
    for part in solution_set:
        print(f" Знайдено сегмент: {part}")
