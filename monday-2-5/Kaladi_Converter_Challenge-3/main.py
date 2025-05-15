

import streamlit as st
from rembg import remove
from PIL import Image
import io
import base64
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import stripe

# Load environment variables
load_dotenv()

# Initialize clients
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEYS")
service_key = os.environ.get("SUPABASE_SERVICE_KEY")
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = os.environ.get("STRIPE_PRICE_ID")  # Add this to your .env

# Validate credentials
if not all([url, key, service_key, STRIPE_PRICE_ID]):
    st.error("Missing required credentials. Please check your .env file")
    st.stop()

# Initialize clients
try:
    supabase = create_client(url, key)
    supabase_admin = create_client(url, service_key)
    # Test connection
    supabase.table('user_credits').select("*").limit(1).execute()
except Exception as e:
    st.error(f"Connection failed: {str(e)}")
    st.stop()

class CreditManager:
    def __init__(self):
        self.free_limit = 5
        self.paid_credits_per_purchase = 10
        self.price_per_purchase = 5  # dollars

    def get_user_credits(self, user_id, user_email):
        try:
            res = supabase.table('user_credits').select('*').eq('id', user_id).execute()

            
            if res.data:
                return res.data[0]
            
            # Create new record with admin client
            new_credits = {
                "id": user_id,
                "email": user_email,
                "free_credits_used": 0,
                "paid_credits": 0
            }
            
            insert_res = supabase_admin.table('user_credits').insert(new_credits).execute()
            return insert_res.data[0]
            
        except Exception as e:
            st.error(f"Error accessing credits: {str(e)}")
            return {"free_credits_used": 0, "paid_credits": 0}

    def use_credit(self, user_id, user_email):
        try:
            credits = self.get_user_credits(user_id, user_email)
            
            if credits['free_credits_used'] < self.free_limit:
                # Use raw SQL increment
                supabase.table('user_credits').update({
                    "free_credits_used": credits['free_credits_used'] + 1
                }).eq('id', user_id).execute()
            else:
                if credits['paid_credits'] <= 0:
                    raise Exception("No credits left")
                # Use raw SQL decrement
                supabase.table('user_credits').update({
                    "paid_credits": credits['paid_credits'] -1 
                }).eq('id', user_id).execute()
            
            # Force UI refresh
            st.session_state.credits_updated = True
                
        except Exception as e:
            st.error(f"Credit usage error: {str(e)}")
            raise

    def create_checkout_session(self, user_email, user_id):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': STRIPE_PRICE_ID,  # Use predefined price ID
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{os.environ.get('BASE_URL')}?payment=success&user_id={user_id}",
                cancel_url=f"{os.environ.get('BASE_URL')}?payment=cancel",
                metadata={
                    'user_id': user_id,
                    'user_email': user_email,
                    'credits': self.paid_credits_per_purchase
                }
            )
            return session.url
        except Exception as e:
            st.error(f"Payment error: {str(e)}")
            return None
        
    
    def add_paid_credits(self, user_id, user_email, credits_to_add=10):
        try:
            credits = self.get_user_credits(user_id, user_email)
            current_credits = credits.get("paid_credits", 0)

            updated_credits = current_credits + credits_to_add

            supabase_admin.table('user_credits').update({
                "paid_credits": updated_credits
            }).eq('id', user_id).execute()

            st.success(f"{credits_to_add} paid credits added successfully!")

        except Exception as e:
            st.error(f"Failed to add credits: {str(e)}")
        

class AuthManager:
    def __init__(self):
        self.session = None

    def sign_up(self, email, password):
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            if not response.user.identities:
                raise Exception("User already exists")
            return True
        except Exception as e:
            st.error(f"Sign up failed: {str(e)}")
            return False

    def sign_in(self, email, password):
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.session_state.user = response.user
            st.session_state.authenticated = True
            st.session_state.show_auth = False
            return True
        except Exception as e:
            st.error(f"Sign in failed: {str(e)}")
            return False

    def sign_out(self):
        try:
            supabase.auth.sign_out()
            st.session_state.clear()
            st.success("Successfully signed out!")
            return True
        except Exception as e:
            st.error(f"Sign out failed: {str(e)}")
            return False

    def get_current_user(self):
        try:
            return supabase.auth.get_user()
        except:
            return None

class BackgroundRemoverApp:
    def __init__(self):
        self.auth = AuthManager()
        self.credit = CreditManager()
        self.setup_page()
        self.setup_styles()

    def setup_page(self):
        st.set_page_config(
            page_title="Background Remover",
            page_icon="🎨",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def setup_styles(self):
        st.markdown("""
        <style>
        .auth-header {
            position: sticky;
            top: 0;
            z-index: 1000;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .credit-info {
           
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

    def show_auth_header(self):
        with st.container():
            st.markdown("<div class='auth-header'>", unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Sign Up", "Sign In"])
            
            with tab1:
                with st.form("signup_form"):
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Create Account"):
                        if self.auth.sign_up(email, password):
                            st.success("Account created! Please check your email and confirm it.")
            
            with tab2:
                with st.form("signin_form"):
                    email = st.text_input("Email", key="signin_email")
                    password = st.text_input("Password", type="password", key="signin_pass")
                    if st.form_submit_button("Sign In"):
                        if self.auth.sign_in(email, password):
                            st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

    def show_main_interface(self):
        st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Kaladi Converter</h1>", unsafe_allow_html=True)
        
        if st.session_state.get('authenticated'):
            user = st.session_state.user
            if st.sidebar.button("🚪 Sign Out"):
                self.auth.sign_out()
                st.rerun()
            st.sidebar.markdown(f"**Logged in as:**\n{user.email}")

        self.show_background_remover()

    def show_background_remover(self):
        st.markdown("## Image Background Remover")
        
        if st.session_state.get('authenticated'):
            user = st.session_state.user
            credits = self.credit.get_user_credits(user.id, user.email)
            remaining_free = max(0, self.credit.free_limit - credits['free_credits_used'])
            total_credits = remaining_free + credits['paid_credits']
            
            # Credit display with color coding
            st.markdown(f"""
            <div class="credit-info">
                <h4>Credits Available</h4>
                <p style="color: {'red' if remaining_free == 0 else 'green'}">
                    Free credits: {remaining_free}/{self.credit.free_limit}
                </p>
                <p style="color: {'red' if credits['paid_credits'] == 0 else 'green'}">
                    Paid credits: {credits['paid_credits']}
                </p>
            </div>
            """, unsafe_allow_html=True)


        uploaded_file = st.file_uploader(
            "Upload Image", 
            type=['png', 'jpg', 'jpeg', 'webp'],
            disabled=not st.session_state.get('authenticated')
        )

        if uploaded_file and st.session_state.get('authenticated'):
            user = st.session_state.user
            col1, col2 = st.columns(2)
            image = Image.open(uploaded_file)
            
            with col1:
                st.image(image, caption="Original Image", use_container_width=True)

            credits = self.credit.get_user_credits(user.id, user.email)
            remaining_free = max(0, self.credit.free_limit - credits['free_credits_used'])
            total_credits = remaining_free + credits['paid_credits']

            if total_credits <= 0:
                st.warning("You've used all your credits. Please purchase more to continue.")
                if st.button(f"Buy {self.credit.paid_credits_per_purchase} credits (${self.credit.price_per_purchase})"):
                    checkout_url = self.credit.create_checkout_session(user.email, user.id)
                    if checkout_url:
                        st.markdown(f"[Click here to complete payment]({checkout_url})", unsafe_allow_html=True)
                return

            if st.button("Remove Background"):
                try:
                    self.credit.use_credit(user.id, user.email)
                    with st.spinner("Processing..."):
                        processed_image = remove(image)
                        st.session_state.processed_image = processed_image
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

            if 'processed_image' in st.session_state:
                with col2:
                    st.image(st.session_state.processed_image, 
                            caption="Processed Image", 
                            use_container_width=True)
                    self.download_processed_image()

    def download_processed_image(self):
        buffered = io.BytesIO()
        st.session_state.processed_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:image/png;base64,{img_str}" download="processed.png">📥 Download Processed Image</a>'
        st.markdown(href, unsafe_allow_html=True)


    def run(self):
        # Handle payment success with new query_params API
        if st.query_params.get("payment") == "success":
            user_id = st.query_params.get("user_id")
            if user_id:
                try:
                    # Add paid credits using admin client
                    # supabase_admin.table('user_credits').update({
                    #     "paid_credits": f"paid_credits + {self.credit.paid_credits_per_purchase}"
                    # }).eq('id', user_id).execute()
                    credit_manager = CreditManager()

                    credit_manager.add_paid_credits(user_id=user_id, user_email=None, credits_to_add=self.credit.paid_credits_per_purchase)


                    st.success(f"Added {self.credit.paid_credits_per_purchase} credits!")
                    st.session_state.credits_updated = True
                    st.query_params.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to add credits: {str(e)}")

        # Check current user status
        user = self.auth.get_current_user()
        if user:
            st.session_state.user = user
            st.session_state.authenticated = True
        
        if not st.session_state.get('authenticated'):
            self.show_auth_header()
        
        self.show_main_interface()

if __name__ == "__main__":
    app = BackgroundRemoverApp()
    app.run()