"use strict";

const BOARD_SIZE = 15;
const EMPTY = 0;
const BLACK = 1;
const WHITE = 2;

const boardElement = document.getElementById("board");
const statusText = document.getElementById("statusText");
const turnStone = document.getElementById("turnStone");
const resetButton = document.getElementById("resetButton");

const resultModal = document.getElementById("resultModal");
const resultTitle = document.getElementById("resultTitle");
const resultMessage = document.getElementById("resultMessage");
const modalResetButton = document.getElementById(
  "modalResetButton"
);

let board = [];
let currentPlayer = BLACK;
let gameOver = false;
let moveCount = 0;
let lastStoneElement = null;

/**
 * 게임 초기화
 */
function initializeGame() {
  board = Array.from(
    { length: BOARD_SIZE },
    () => Array(BOARD_SIZE).fill(EMPTY)
  );

  currentPlayer = BLACK;
  gameOver = false;
  moveCount = 0;
  lastStoneElement = null;

  boardElement.innerHTML = "";
  resultModal.classList.add("hidden");

  createBoard();
  updateStatus();
}

/**
 * 15×15 오목판 생성
 */
function createBoard() {
  const starPoints = new Set([
    "3-3",
    "3-11",
    "7-7",
    "11-3",
    "11-11"
  ]);

  for (let row = 0; row < BOARD_SIZE; row += 1) {
    for (let col = 0; col < BOARD_SIZE; col += 1) {
      const point = document.createElement("button");

      point.type = "button";
      point.className = "point";

      point.dataset.row = String(row);
      point.dataset.col = String(col);

      point.setAttribute("role", "gridcell");
      point.setAttribute(
        "aria-label",
        `${row + 1}행 ${col + 1}열`
      );

      const pointKey = `${row}-${col}`;

      if (starPoints.has(pointKey)) {
        point.classList.add("star-point");

        const star = document.createElement("span");
        star.className = "star";

        point.appendChild(star);
      }

      point.addEventListener("click", handlePointClick);
      boardElement.appendChild(point);
    }
  }
}

/**
 * 바둑판 클릭 처리
 */
function handlePointClick(event) {
  if (gameOver) {
    return;
  }

  const point = event.currentTarget;
  const row = Number(point.dataset.row);
  const col = Number(point.dataset.col);

  if (board[row][col] !== EMPTY) {
    statusText.textContent =
      "이미 돌이 놓인 자리입니다. 다른 곳을 선택하세요.";

    return;
  }

  placeStone(point, row, col);
}

/**
 * 선택한 위치에 돌 놓기
 */
function placeStone(point, row, col) {
  board[row][col] = currentPlayer;
  moveCount += 1;

  if (lastStoneElement) {
    lastStoneElement.classList.remove("last-move");
  }

  const stone = document.createElement("span");

  stone.classList.add(
    "stone",
    currentPlayer === BLACK ? "black" : "white",
    "last-move"
  );

  point.appendChild(stone);
  point.classList.add("occupied");

  point.setAttribute(
    "aria-label",
    `${row + 1}행 ${col + 1}열 ${
      currentPlayer === BLACK ? "흑돌" : "백돌"
    }`
  );

  lastStoneElement = stone;

  if (checkWin(row, col, currentPlayer)) {
    finishGame(currentPlayer);
    return;
  }

  if (moveCount === BOARD_SIZE * BOARD_SIZE) {
    finishDraw();
    return;
  }

  currentPlayer =
    currentPlayer === BLACK ? WHITE : BLACK;

  updateStatus();
}

/**
 * 현재 차례 표시
 */
function updateStatus() {
  const isBlackTurn = currentPlayer === BLACK;

  statusText.textContent = isBlackTurn
    ? "흑돌 차례입니다."
    : "백돌 차례입니다.";

  turnStone.classList.toggle("black", isBlackTurn);
  turnStone.classList.toggle("white", !isBlackTurn);
}

/**
 * 승리 여부 검사
 *
 * 검사 방향:
 * 1. 가로
 * 2. 세로
 * 3. 왼쪽 위 ↘ 오른쪽 아래
 * 4. 오른쪽 위 ↙ 왼쪽 아래
 */
function checkWin(row, col, player) {
  const directions = [
    [0, 1],
    [1, 0],
    [1, 1],
    [1, -1]
  ];

  return directions.some(([rowDirection, colDirection]) => {
    const connectedCount =
      1 +
      countStones(
        row,
        col,
        rowDirection,
        colDirection,
        player
      ) +
      countStones(
        row,
        col,
        -rowDirection,
        -colDirection,
        player
      );

    return connectedCount >= 5;
  });
}

/**
 * 특정 방향으로 같은 돌 개수 계산
 */
function countStones(
  startRow,
  startCol,
  rowDirection,
  colDirection,
  player
) {
  let count = 0;
  let row = startRow + rowDirection;
  let col = startCol + colDirection;

  while (
    isInsideBoard(row, col) &&
    board[row][col] === player
  ) {
    count += 1;
    row += rowDirection;
    col += colDirection;
  }

  return count;
}

/**
 * 좌표가 바둑판 안에 있는지 확인
 */
function isInsideBoard(row, col) {
  return (
    row >= 0 &&
    row < BOARD_SIZE &&
    col >= 0 &&
    col < BOARD_SIZE
  );
}

/**
 * 승리 처리
 */
function finishGame(winner) {
  gameOver = true;

  const winnerName =
    winner === BLACK ? "흑돌" : "백돌";

  statusText.textContent = `${winnerName}이 승리했습니다!`;

  resultTitle.textContent = `${winnerName} 승리!`;
  resultMessage.textContent =
    `${winnerName}이 돌 5개를 연결했습니다.`;

  resultModal.classList.remove("hidden");
}

/**
 * 무승부 처리
 */
function finishDraw() {
  gameOver = true;

  statusText.textContent = "무승부입니다.";

  resultTitle.textContent = "무승부";
  resultMessage.textContent =
    "바둑판이 모두 찼지만 승자가 없습니다.";

  resultModal.classList.remove("hidden");
}

/**
 * 다시 시작
 */
function resetGame() {
  initializeGame();
}

resetButton.addEventListener("click", resetGame);
modalResetButton.addEventListener("click", resetGame);

/* 처음 게임 실행 */
initializeGame();