import sys
from streamlit.web import cli as stcli

if __name__ == '__main__':
    # Sanki terminale "streamlit run app.py" yazmışız gibi davranmasını sağlıyoruz
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())