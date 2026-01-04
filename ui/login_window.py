# ui/login_window.py

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMessageBox, QStackedWidget, QWidget, QFrame, QSizePolicy, QToolButton)
# QPixmap is needed for the robust background image handling
from PySide6.QtGui import QIcon, QPainter, QLinearGradient, QColor, QPixmap
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect

from database.database_manager import create_user, check_user


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign In - Freelancer's Business Hub")
        self.setWindowFlags(Qt.Window)
        self.setMinimumSize(900, 600)
        self.setObjectName("LoginWindow")

        # --- Main Layout ---
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addStretch(1)

        # --- Glass Effect Frame ---
        self.glass_frame = QFrame() # Made it a class attribute for resizeEvent
        self.glass_frame.setObjectName("GlassFrame")
        self.glass_frame.setFixedSize(420, 500)
        self.glass_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        frame_layout = QVBoxLayout(self.glass_frame)
        frame_layout.setContentsMargins(35, 35, 35, 35)
        frame_layout.setSpacing(15)

        # --- Stacked Widget to switch between Login and Register ---
        self.stacked_widget = QStackedWidget()
        frame_layout.addWidget(self.stacked_widget)

        # Add login and register widgets
        self.login_widget = QWidget()
        self.setup_login_ui()
        self.stacked_widget.addWidget(self.login_widget)

        self.register_widget = QWidget()
        self.setup_register_ui()
        self.stacked_widget.addWidget(self.register_widget)

        main_layout.addWidget(self.glass_frame)
        main_layout.addStretch(1)

        # --- Apply Styles ---
        self.setStyleSheet(self.styles())

    def setup_login_ui(self):
        layout = QVBoxLayout(self.login_widget)
        icon_label = QLabel()
        icon_label.setPixmap(QIcon("assets/icons/briefcase.svg").pixmap(QSize(40, 40)))
        icon_label.setAlignment(Qt.AlignCenter)

        title = QLabel("Sign in with email")
        title.setObjectName("LoginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Make a new doc to bring your words, data, and teams together.")
        subtitle.setObjectName("LoginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        self.login_user_input_widget, self.login_user_input = self.create_input_field("assets/icons/user.svg", "Username")
        self.login_pass_input_widget, self.login_pass_input = self.create_input_field("assets/icons/lock.svg", "Password", is_password=True)

        login_button = QPushButton("Get Started")
        login_button.setObjectName("LoginButton")

        show_register_button = QPushButton("Or sign up")
        show_register_button.setObjectName("LinkButton")

        layout.addWidget(icon_label)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch(1)
        layout.addWidget(self.login_user_input_widget)
        layout.addWidget(self.login_pass_input_widget)
        layout.addStretch(1)
        layout.addWidget(login_button)
        layout.addWidget(show_register_button)

        login_button.clicked.connect(self.handle_login)
        show_register_button.clicked.connect(lambda: self.animate_switch(1))

    def setup_register_ui(self):
        layout = QVBoxLayout(self.register_widget)
        title = QLabel("Create a New Account")
        title.setObjectName("LoginTitle")
        title.setAlignment(Qt.AlignCenter)

        self.reg_user_input_widget, self.reg_user_input = self.create_input_field("assets/icons/user.svg", "Username")
        self.reg_pass_input_widget, self.reg_pass_input = self.create_input_field("assets/icons/lock.svg", "New Password", is_password=True)
        self.reg_confirm_pass_widget, self.reg_confirm_pass_input = self.create_input_field("assets/icons/lock.svg", "Confirm Password", is_password=True)

        register_button = QPushButton("Register Account")
        register_button.setObjectName("LoginButton")

        show_login_button = QPushButton("Back to Login")
        show_login_button.setObjectName("LinkButton")

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.reg_user_input_widget)
        layout.addWidget(self.reg_pass_input_widget)
        layout.addWidget(self.reg_confirm_pass_widget)
        layout.addStretch(1)
        layout.addWidget(register_button)
        layout.addWidget(show_login_button)

        register_button.clicked.connect(self.handle_register)
        show_login_button.clicked.connect(lambda: self.animate_switch(0))

    def create_input_field(self, icon_path, placeholder, is_password=False):
        frame = QFrame()
        frame.setObjectName("LoginInputFrame")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 5, 10, 5)

        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(20, 20)))

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setObjectName("LoginLineEdit")
        line_edit.setStyleSheet("color: #ffffff;")

        if is_password:
            line_edit.setEchoMode(QLineEdit.Password)
            eye_button = QToolButton()
            eye_button.setIcon(QIcon("assets/icons/eye.svg"))
            eye_button.setCheckable(True)
            eye_button.setStyleSheet("background: transparent; border: none;")
            eye_button.setIconSize(QSize(18, 18))

            def toggle_password():
                if eye_button.isChecked():
                    line_edit.setEchoMode(QLineEdit.Normal)
                    eye_button.setIcon(QIcon("assets/icons/eye-off.svg"))
                else:
                    line_edit.setEchoMode(QLineEdit.Password)
                    eye_button.setIcon(QIcon("assets/icons/eye.svg"))

            eye_button.clicked.connect(toggle_password)
            layout.addWidget(icon_label)
            layout.addWidget(line_edit)
            layout.addWidget(eye_button)
        else:
            layout.addWidget(icon_label)
            layout.addWidget(line_edit)

        return frame, line_edit

    def animate_switch(self, index):
        current_index = self.stacked_widget.currentIndex()
        if current_index == index: return

        current_widget = self.stacked_widget.currentWidget()
        next_widget = self.stacked_widget.widget(index)
        width = self.stacked_widget.frameGeometry().width()
        next_widget.setGeometry(QRect(width if index > current_index else -width, 0, width, self.stacked_widget.height()))
        next_widget.show()

        anim_out = QPropertyAnimation(current_widget, b"geometry")
        anim_out.setDuration(300); anim_out.setEasingCurve(QEasingCurve.InOutCubic)
        anim_out.setStartValue(current_widget.geometry())
        anim_out.setEndValue(QRect(-width if index > current_index else width, 0, width, current_widget.height()))

        anim_in = QPropertyAnimation(next_widget, b"geometry")
        anim_in.setDuration(300); anim_in.setEasingCurve(QEasingCurve.InOutCubic)
        anim_in.setStartValue(next_widget.geometry())
        anim_in.setEndValue(QRect(0, 0, width, next_widget.height()))

        anim_out.start(); anim_in.start()
        self.stacked_widget.setCurrentIndex(index)

    # --- THIS IS THE FINAL, ROBUST VERSION OF paintEvent ---
    def paintEvent(self, event):
        """Draws the background, preferring an image but falling back to a gradient."""
        painter = QPainter()
        # It is critical to begin the painter ON the widget itself ('self')
        if not painter.begin(self):
            print("CRITICAL ERROR: QPainter could not be initialized on LoginWindow.")
            return

        # First, try to load the background image
        background_pixmap = QPixmap("assets/background.jpg")

        # Check if the image loaded successfully (is not null)
        if not background_pixmap.isNull():
            # If the image is valid, draw it scaled to fill the entire window
            scaled_pixmap = background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(self.rect(), scaled_pixmap)
        else:
            # If the image FAILED to load, print a warning and draw your gradient as a fallback
            print("WARNING: Could not load 'assets/background.jpg'. Drawing fallback gradient.")
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor("#667eea"))
            gradient.setColorAt(1, QColor("#764ba2"))
            painter.fillRect(self.rect(), gradient)
        
        # It is critical to end the painter
        painter.end()

    def resizeEvent(self, event):
        win_width = self.width(); win_height = self.height()
        card_width = min(420 + (win_width - 900) // 10, 550)
        card_height = min(500 + (win_height - 600) // 10, 600)
        self.glass_frame.setFixedSize(card_width, card_height)

    def styles(self):
        return """
        #LoginWindow {
            /* The background is handled by paintEvent */
            background-color: #1e1e2f; 
        }
        #GlassFrame {
            background-color: rgba(24, 24, 37, 0.65); /* Darker glass */
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        #LoginTitle {
            font-size: 26px;
            font-weight: bold;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            margin-bottom: 5px;
        }
        #LoginSubtitle {
            font-size: 14px;
            color: #bac2de;
            font-family: 'Segoe UI', sans-serif;
        }
        #LoginInputFrame {
            background-color: rgba(0, 0, 0, 0.3); /* Dark input container */
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        #LoginLineEdit {
            background: transparent;
            border: none;
            font-size: 15px;
            color: #ffffff;
            padding: 2px;
        }
        #LoginButton {
            background-color: #89b4fa; /* Primary Blue */
            color: #1e1e2f; /* Dark Text */
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            padding: 12px;
            border: none;
        }
        #LoginButton:hover {
            background-color: #b4befe;
        }
        #LoginButton:pressed {
            background-color: #74c7ec;
        }
        #LinkButton {
            background: none;
            border: none;
            color: #89b4fa;
            font-weight: bold;
            font-size: 13px;
        }
        #LinkButton:hover {
            text-decoration: underline;
            color: #b4befe;
        }
        """

    def handle_login(self):
        username = self.login_user_input.text()
        password = self.login_pass_input.text()
        if check_user(username, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "The username or password you entered is incorrect.")

    def handle_register(self):
        username = self.reg_user_input.text()
        password = self.reg_pass_input.text()
        confirm_password = self.reg_confirm_pass_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty."); return
        if len(password) < 8:
            QMessageBox.warning(self, "Password Error", "Password must be at least 8 characters long."); return
        if password != confirm_password:
            QMessageBox.warning(self, "Password Error", "Passwords do not match."); return

        if create_user(username, password):
            QMessageBox.information(self, "Success", "Account created successfully! Please login.")
            self.animate_switch(0)
        else:
            QMessageBox.warning(self, "Registration Failed", "That username already exists. Please choose another.")