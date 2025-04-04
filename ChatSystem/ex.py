import streamlit as st
import socket
import time

# Streamlit UI Setup
st.title("Real-Time Chat Application")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'client' not in st.session_state:
    st.session_state.client = None
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'last_check' not in st.session_state:
    st.session_state.last_check = time.time()
if 'message_sent' not in st.session_state:
    st.session_state.message_sent = False

# Input for nickname
nickname = st.text_input("Enter your username:", key="nickname")

# Function to check for new messages
def check_for_messages():
    if not st.session_state.connected or not st.session_state.client:
        return
        
    # Make the socket non-blocking
    st.session_state.client.setblocking(False)
    
    try:
        # Try to receive messages
        while True:
            try:
                message = st.session_state.client.recv(1024).decode('utf-8')
                if message:
                    # Skip the NICK command - don't display it in chat
                    if message != "NICK":
                        st.session_state.messages.append(message)
            except BlockingIOError:
                # No more messages to read
                break
            except Exception as e:
                st.error(f"Error receiving message: {e}")
                st.session_state.connected = False
                break
    finally:
        # Set back to blocking for other operations
        st.session_state.client.setblocking(True)

# Connect to server function
def connect_to_server():
    if st.session_state.connected:
        st.warning("Already connected!")
        return
        
    try:
        # Create socket and connect
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5555))
        
        # Handle the NICK command from server
        initial_msg = client.recv(1024).decode('utf-8')
        if initial_msg == "NICK":
            # Send nickname
            client.send(nickname.encode('utf-8'))
        else:
            # Unexpected first message, handle appropriately
            st.error(f"Unexpected initial message from server: {initial_msg}")
            return
        
        # Update session state
        st.session_state.client = client
        st.session_state.connected = True
        
        # Receive welcome message
        welcome_msg = client.recv(1024).decode('utf-8')
        st.session_state.messages.append(welcome_msg)
            
        st.success("Connected to the chat server!")
    except Exception as e:
        st.error(f"Connection failed: {e}")
        st.session_state.client = None
        st.session_state.connected = False

# Connect button
if st.button("Connect") and nickname and not st.session_state.connected:
    connect_to_server()

# Disconnect function
def disconnect():
    if st.session_state.client:
        try:
            st.session_state.connected = False
            st.session_state.client.close()
            st.session_state.client = None
            st.success("Disconnected from server")
        except Exception as e:
            st.error(f"Error disconnecting: {e}")

# Disconnect button
if st.button("Disconnect") and st.session_state.connected:
    disconnect()

# Check for messages regularly
if st.session_state.connected:
    # Check for new messages every time the app reruns
    check_for_messages()

# Function to handle sending messages
def send_message():
    if st.session_state.message and st.session_state.connected:
        try:
            full_message = f'{nickname}: {st.session_state.message}'
            st.session_state.client.send(full_message.encode('utf-8'))
            # Record our own message
            
            # Set flag to clear the input on next rerun
            st.session_state.message_sent = True
        except Exception as e:
            st.error(f"Failed to send message: {e}")
            st.session_state.connected = False

# Clear the message input after sending
if st.session_state.message_sent:
    st.session_state.message = ""
    st.session_state.message_sent = False

# Message Input & Sending
message = st.text_input("Type your message:", key="message")

# Send button
if st.button("Send") and message and st.session_state.connected:
    send_message()
    st.rerun()  # Force a rerun to clear the input

# Force a rerun every few seconds to check for new messages
if st.session_state.connected:
    current_time = time.time()
    if current_time - st.session_state.last_check > 1:  # Check every second
        st.session_state.last_check = current_time
        time.sleep(0.1)  # Small delay
        st.rerun()

# Display Chat Messages
st.subheader("Chat Messages")
chat_container = st.container()
with chat_container:
    for idx, msg in enumerate(st.session_state.messages):
        st.text(f"{msg}")

# Add a status indicator
if st.session_state.connected:
    st.success("Connected to chat server")
else:
    st.warning("Not connected to chat server")

# Add manual refresh button
if st.button("Refresh Chat"):
    check_for_messages()
    st.rerun()