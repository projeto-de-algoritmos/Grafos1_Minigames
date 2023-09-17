#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <iostream>

const int windowSize = 300;
const int gridSize = windowSize / 3;

sf::RenderWindow window(sf::VideoMode(windowSize, windowSize), "Jogo da Velha");
sf::Font font;

enum class CellState { Empty, X, O };

class TicTacToe {
public:
    TicTacToe() : currentPlayer(CellState::X), game_over(false) {
        board.resize(3, std::vector<CellState>(3, CellState::Empty));
    }

    void draw() {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                sf::RectangleShape cell(sf::Vector2f(gridSize, gridSize));
                cell.setPosition(i * gridSize, j * gridSize);
                cell.setOutlineThickness(2);
                cell.setOutlineColor(sf::Color::Black);

                if (board[i][j] == CellState::X) {
                    sf::Text text("X", font, gridSize / 1.5);
                    text.setPosition(i * gridSize + gridSize / 4, j * gridSize);
                    window.draw(text);
                }
                else if (board[i][j] == CellState::O) {
                    sf::Text text("O", font, gridSize / 1.5);
                    text.setPosition(i * gridSize + gridSize / 4, j * gridSize);
                    window.draw(text);
                }
                window.draw(cell);
            }
        }
    }

    bool makeMove(int row, int col) {
        if (board[row][col] == CellState::Empty && !game_over) {
            board[row][col] = currentPlayer;
            currentPlayer = (currentPlayer == CellState::X) ? CellState::O : CellState::X;
            return true;
        }
        return false;
    }

    bool checkWin(CellState player) {
        for (int i = 0; i < 3; ++i) {
            if (board[i][0] == player && board[i][1] == player && board[i][2] == player) {
                return true;
            }
            if (board[0][i] == player && board[1][i] == player && board[2][i] == player) {
                return true;
            }
        }
        if (board[0][0] == player && board[1][1] == player && board[2][2] == player) {
            return true;
        }
        if (board[0][2] == player && board[1][1] == player && board[2][0] == player) {
            return true;
        }
        return false;
    }

    bool checkDraw() {
        for (const auto& row : board) {
            for (const auto& cell : row) {
                if (cell == CellState::Empty) {
                    return false;
                }
            }
        }
        return true;
    }

    bool isGameOver() const {
        return game_over;
    }

    void setGameOver(bool value) {
        game_over = value;
    }

private:
    std::vector<std::vector<CellState>> board;
    CellState currentPlayer;
    bool game_over;
};

int main() {
    TicTacToe game;

    if (!font.loadFromFile("arial.ttf")) {
        std::cerr << "Font file not found!" << std::endl;
        return 1;
    }

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
            if (!game.isGameOver() && event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Left) {
                int x = event.mouseButton.x / gridSize;
                int y = event.mouseButton.y / gridSize;
                if (x >= 0 && x < 3 && y >= 0 && y < 3) {
                    if (game.makeMove(x, y)) {
                        if (game.checkWin(CellState::X)) {
                            game.setGameOver(true);
                            std::cout << "Jogador X ganhou!" << std::endl;
                        }
                        else if (game.checkDraw()) {
                            game.setGameOver(true);
                            std::cout << "Empate!" << std::endl;
                        }
                    }
                }
            }
        }

        window.clear(sf::Color::White);
        game.draw();
        window.display();
    }

    return 0;
}
