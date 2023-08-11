import streamlit as st
import random
import string


class PasswordGenerator:
    def __init__(self, length):
        self.length = length
        self.saved_passwords = []

    def generate_password(self, *charsets):
        result = [random.choice(random.choice(charsets))
                  for _ in range(self.length)]
        password = ''.join(result)
        self.saved_passwords.append(password)
        if len(self.saved_passwords) > 10:
            self.saved_passwords.pop(0)
        return password

    def digits(self):
        return self.generate_password(string.digits)

    def bd_digits(self):
        return self.generate_password(string.ascii_uppercase, string.digits)

    def sd_digits(self):
        return self.generate_password(string.ascii_lowercase, string.digits)

    def sbd_digits(self):
        return self.generate_password(string.ascii_lowercase, string.ascii_uppercase, string.digits)


def main():
    st.set_page_config(
        page_title="**SecurePass Generator**",
        page_icon="🔒",
        layout="wide"

    )

    st.title("SecurePass Generator")
    st.markdown(
        "**Create :red[Strong] and :blue[Secure] passwords with ease.**")

    password_length = st.sidebar.slider("Password Length", 8, 24, 12)
    password_generator = PasswordGenerator(password_length)

    option = st.sidebar.selectbox("Select an Option",
                                  ["Digits", "Capital + Digits", "Small + Digits", "All Characters", "Saved Passwords"])

    st.sidebar.markdown("### Password Options")
    include_special_chars = st.sidebar.checkbox("Include Special Characters")
    include_similar_chars = st.sidebar.checkbox(
        "Exclude Similar Characters (e.g., 'I', 'l', '1', 'O', '0')")

    st.sidebar.markdown("### Privacy and Security")
    st.sidebar.info(
        "Your generated passwords are not stored or tracked. They only reside in your current session.")

    if option == "Digits":
        password = password_generator.digits()

    elif option == "Capital + Digits":
        password = password_generator.bd_digits()

    elif option == "Small + Digits":
        password = password_generator.sd_digits()

    elif option == "All Characters":
        charsets = [string.ascii_lowercase,
                    string.ascii_uppercase, string.digits]
        if include_special_chars:
            charsets.append(string.punctuation)
        password = password_generator.generate_password(*charsets)

        if include_similar_chars:
            password = password.replace('I', '').replace('l', '').replace(
                '1', '').replace('O', '').replace('0', '')

    elif option == "Saved Passwords":
        st.title("Saved Passwords")
        saved_passwords = password_generator.saved_passwords
        if saved_passwords:
            for idx, password in enumerate(saved_passwords):
                st.write(f"{idx + 1}. {password}")
        else:
            st.write("No passwords saved yet.")
        return

    st.subheader("Generated Password")
    st.markdown(
        f"<p style='font-size: 24px;color:#007BFF;'>{password}</p>", unsafe_allow_html=True)
    if st.button("Copy Password"):
        pyperclip.copy(password)
        st.success("Password copied to clipboard!")


if __name__ == "__main__":
    main()
