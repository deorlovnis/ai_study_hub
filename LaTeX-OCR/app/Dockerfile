FROM wildedav/vllm-deepseek-ocr:gundam-af61d70

WORKDIR /app

COPY . .

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /root/.local/bin/uv pip install --system -U vllm --pre --extra-index-url https://wheels.vllm.ai/nightly && \
    /root/.local/bin/uv pip install --system .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
