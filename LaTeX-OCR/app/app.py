import streamlit as st
from PIL import Image

from src.adapters import VllmOcrLatexAdapter
from src.llm_factory import create_llm
from src.services import OcrService


@st.cache_resource(show_spinner=False)
def load_ocr_service() -> OcrService:
    """Load the OCR service, caching the model."""
    with st.spinner("Loading OCR model (first run may take a moment)..."):
        try:
            llm = create_llm()
            adapter = VllmOcrLatexAdapter(llm)
            service = OcrService(adapter)
            return service
        except Exception as exc:
            raise RuntimeError("Failed to load the OCR model.") from exc

st.set_page_config(
    page_title="LaTeX OCR with DeepSeek",
    page_icon="🐋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("LaTeX OCR with DeepSeek")

st.markdown('<p style="margin-top: -20px;">Extract LaTeX code from images using DeepSeek!</p>', unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        uploaded_file.seek(0)
        image_bytes = uploaded_file.getvalue()
        st.image(image_bytes, caption="Uploaded Image")
        if st.button("Extract LaTeX", use_container_width=True):
            try:
                service = load_ocr_service()
                with st.spinner("Processing image..."):
                    st.session_state['ocr_result'] = service.extract_latex_from_image(image_bytes)
            except (RuntimeError, ValueError) as err:
                st.error(str(err))
            except Exception as err:
                st.error(f"An unexpected error occurred: {err}")
        if st.button("Clear", use_container_width=True):
            if 'ocr_result' in st.session_state:
                del st.session_state['ocr_result']
            st.rerun()

if 'ocr_result' in st.session_state:
    st.markdown("### LaTeX Code")
    st.code(st.session_state['ocr_result'], language='latex')

    st.markdown("### Rendered LaTeX")
    cleaned_latex = st.session_state['ocr_result'].replace(r"\[", "").replace(r"\]", "")
    st.latex(cleaned_latex)
else:
    st.info("Upload an image and click 'Extract LaTeX' to see the results.")