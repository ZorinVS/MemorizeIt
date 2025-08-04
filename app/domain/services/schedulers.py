from abc import ABC, abstractmethod


class RepetitionScheduler(ABC):
    """Абстрактный алгоритм расчета повторений.

    Определяет интерфейс для алгоритмов, которые на основе оценки
    пользователя рассчитывают параметры следующего повторения карточки.
    """

    @abstractmethod
    def init(self) -> tuple[int, float, int]:
        """Возвращает стартовые параметры повторения.

        Returns:
            Кортеж из следующих параметров:
                - Интервал (в днях).
                - Коэффициент лёгкости.
                - Количество успешных повторений подряд.
        """
        pass

    @abstractmethod
    def update(self, score: int, n: int, ef: float, interval: int) -> tuple[int, float, int]:
        """Рассчитывает параметры следующего повторения.

        Args:
            score: Оценка запоминания (0 — не вспомнил, 1 — с трудом, 2 — легко).
            n: Количество успешных повторений подряд.
            ef: Текущий коэффициент лёгкости (Easiness Factor).
            interval: Интервал до следующего повторения в днях.

        Returns:
            Кортеж из следующих параметров повторения:
                - Новый интервал (в днях).
                - Новый коэффициент лёгкости.
                - Обновлённое число повторений подряд.
        """
        pass


class SimplifiedSM2Scheduler(RepetitionScheduler):
    """Упрощённая реализация алгоритма SM-2 для интервального повторения.

    Attributes:
        INITIAL_N: Начальное количество успешных повторений.
        MIN_EF: Минимально допустимое значение коэффициента лёгкости (EF).
        DEFAULT_EF: Стартовое значение коэффициента лёгкости.
        DEFAULT_INTERVALS: Интервалы (в днях) для первых двух повторений.
        EF_DELTA: Изменения коэффициента лёгкости в зависимости от оценки (0–2).
    """
    INITIAL_N: int = 0
    MIN_EF: float = 1.3
    DEFAULT_EF: float = 2.5
    DEFAULT_INTERVALS: tuple[int, int] = (1, 6)
    EF_DELTA: dict[int, float] = {0: -0.8, 1: -0.4, 2: 0.1}

    def init(self) -> tuple[int, float, int]:
        """Возвращает стартовые параметры повторения по умолчанию.

        Returns:
            Кортеж из следующих параметров:
                - Интервал (в днях).
                - Стартовый коэффициент лёгкости.
                - Начальное количество успешных повторений подряд.
        """
        return self.DEFAULT_INTERVALS[0], self.DEFAULT_EF, self.INITIAL_N

    def update(self, score: int, n: int, ef: float, interval: int) -> tuple[int, float, int]:
        """Рассчитывает параметры следующего повторения по упрощённой схеме SM-2.

        Args:
            score: Оценка воспроизведения (0 — не вспомнил, 1 — с трудом, 2 — легко).
            n: Количество успешных повторений подряд.
            ef: Текущий коэффициент лёгкости (Easiness Factor).
            interval: Интервал до следующего повторения в днях.

        Returns:
            Кортеж из следующих параметров повторения:
                - Новый интервал (в днях).
                - Новый коэффициент лёгкости.
                - Обновлённое число повторений подряд.
        """
        if score == 0:
            n = self.INITIAL_N
            interval = self.DEFAULT_INTERVALS[n]
            ef = self._change_ef(ef, score)
            return interval, ef, n

        if n in {0, 1}:
            interval = self.DEFAULT_INTERVALS[n]
        else:
            interval = round(interval * ef)

        ef = self._change_ef(ef, score)
        n += 1
        return interval, ef, n

    def _change_ef(self, current_ef: float, score: int) -> float:
        """Корректирует коэффициент лёгкости (EF) в зависимости от оценки.

        Args:
            current_ef: Текущее значение коэффициента лёгкости.
            score: Оценка запоминания.

        Returns:
            Новое значение коэффициента, ограниченное минимумом MIN_EF.
        """
        new_ef = current_ef + self.EF_DELTA[score]
        return max(new_ef, self.MIN_EF)
