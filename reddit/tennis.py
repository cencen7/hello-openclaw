"""
第一问：设计一个游戏，设计三个方法，加比分，查比分，查结果。只有2个player。
第二问写了个match的class然后在里面build game object。
需要自己写和跑test case，要求需要能够跑通。感觉考察的是OOD能力。

设计一个游戏，设计三个方法，加比分，查比分，查结果。
同时，还有几个别的要求：

必须领先两分才算胜利。如果比分超过三比三，要重置为三比三（比如四比四，五比五就要重置）
第二问转化成human score， love, deuce， 参考网球比分规则

整体来说不难，地里的经典题目，网球比分。
第一问，按照要求来就行，输出两人分数，谁是winner。
第二问， 把分数变成human score，比如30-30， 就是“deuce”。


两个人玩一个游戏，A 赢 则 A 积一分，完成以下函数：
1 输出两个人当前比分
2 积分函数，A 赢则积1分，B赢则B积分， 如果超过3比3 并且比分相同则重置比分为3：3. 如果已有获胜者 继续调这个函数则返回error。
3 winner 函数， 如果A 超过5分并且领先 B 2分 则A获胜输出A。 如果比赛没有获胜者，这个函数要返回 error
I wrote a Game class with all the methods, increment, current_score
Part2:
还是这个游戏 但是要玩5局。 谁先赢3局算赢。 更新并扩展你的函数。
GameSet
只有一个play函数，所有的logic都在这个函数里面，有一个循环，结束条件时5局或者有一个赢了三局。
在这个loop里面，创建一个game对象，然后调用increment多次，直到游戏结束。

电面，网球比赛那道题，两问。第一问写了个game的class，第二问写了个match的class然后在里面build game object
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Iterator, Optional, Tuple, List


class Player(str, Enum):
    A = "A"
    B = "B"


@dataclass
class Game:
    a: int = 0
    b: int = 0

    def point(self, winner: Player) -> None:
        """Add one point to winner. Illegal if game already ended."""
        if self.winner() is not None:
            raise RuntimeError("Game already has a winner")

        if winner == Player.A:
            self.a += 1
        elif winner == Player.B:
            self.b += 1
        else:
            raise ValueError("Invalid player")

        # Custom rule: if tied and both > 3, reset to 3-3
        if self.a == self.b and self.a > 3:
            self.a = self.b = 3

    def score(self) -> Tuple[int, int]:
        return self.a, self.b

    def winner(self) -> Optional[Player]:
        """Return winner if exists, else None (normal state)."""
        if self.a >= 5 and self.a - self.b >= 2:
            return Player.A
        if self.b >= 5 and self.b - self.a >= 2:
            return Player.B
        return None


@dataclass
class Match:
    max_games: int = 5
    games_to_win: int = 3

    def play(self, point_winners: Iterable[Player]) -> Player:
        it: Iterator[Player] = iter(point_winners)
        a_games = b_games = 0
        games_played = 0

        while games_played < self.max_games and a_games < self.games_to_win and b_games < self.games_to_win:
            game = Game()

            # play a single game until it ends
            gw: Optional[Player] = None
            while gw is None:
                try:
                    p = next(it)
                except StopIteration:
                    raise RuntimeError("Not enough points to finish the match")
                game.point(p)
                gw = game.winner()

            # record game winner
            if gw == Player.A:
                a_games += 1
            else:
                b_games += 1
            games_played += 1

        # decide match winner
        if a_games >= self.games_to_win:
            return Player.A
        if b_games >= self.games_to_win:
            return Player.B

        # max games reached: higher games wins
        if a_games > b_games:
            return Player.A
        if b_games > a_games:
            return Player.B

        raise RuntimeError("Match ended tied (unexpected under these rules)")


# ---------------- Tests ----------------

def assert_raises(expected_exc, fn, msg=""):
    try:
        fn()
    except expected_exc:
        return
    except Exception as e:
        raise AssertionError(f"{msg} Expected {expected_exc.__name__}, got {type(e).__name__}: {e}") from e
    raise AssertionError(f"{msg} Expected {expected_exc.__name__} but no exception was raised.")


def make_game_points(winner: Player) -> List[Player]:
    # Bring to 3:3 then winner wins two points => 5:3
    seq: List[Player] = []
    for _ in range(3):
        seq += [Player.A, Player.B]
    seq += [winner, winner]
    return seq


def test_game_reset_at_4_4():
    g = Game()
    for _ in range(4):
        g.point(Player.A)
        g.point(Player.B)
    assert g.score() == (3, 3)


def test_game_win_and_no_more_points():
    g = Game()
    for p in make_game_points(Player.A):
        g.point(p)
    assert g.score() == (5, 3)
    assert g.winner() == Player.A
    assert_raises(RuntimeError, lambda: g.point(Player.B), "cannot point after game ends. ")


def test_match_a_wins_3_0():
    m = Match()
    points = make_game_points(Player.A) * 3
    assert m.play(points) == Player.A


def test_match_b_wins_3_2():
    m = Match()
    points = (
        make_game_points(Player.A) +
        make_game_points(Player.B) +
        make_game_points(Player.A) +
        make_game_points(Player.B) +
        make_game_points(Player.B)
    )
    assert m.play(points) == Player.B


def test_match_runs_out_of_points():
    m = Match()
    points = make_game_points(Player.A)  # only enough for 1 game
    assert_raises(RuntimeError, lambda: m.play(points), "should run out of points. ")


def run_all_tests():
    test_game_reset_at_4_4()
    test_game_win_and_no_more_points()
    test_match_a_wins_3_0()
    test_match_b_wins_3_2()
    test_match_runs_out_of_points()
    print("All tests passed ✅")


if __name__ == "__main__":
    run_all_tests()
