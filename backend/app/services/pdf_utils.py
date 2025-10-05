import os
import httpx
from pathlib import Path

TMP_DIR = Path(__file__).parent / "tmp"

async def download_arxiv_pdfs(papers):
    """
    Downloads PDFs for a list of arXiv papers to a temporary folder.
    Each paper dict must have an 'id' field (e.g., 'http://arxiv.org/abs/1234.5678').
    Returns a list of file paths to the downloaded PDFs.
    """
    # Create tmp folder
    TMP_DIR.mkdir(exist_ok=True)
    pdf_paths = []
    for paper in papers:
        arxiv_id = paper["id"].split("/")[-1]
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        pdf_path = TMP_DIR / f"{arxiv_id}.pdf"
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(pdf_url)
                # If we get a redirect with a relative location, retry with the correct URL
                if response.status_code in (301, 302) and "location" in response.headers:
                    location = response.headers["location"]
                    if location.startswith("/"):
                        pdf_url_retry = f"https://arxiv.org{location}"
                    else:
                        pdf_url_retry = location
                    response = await client.get(pdf_url_retry)
                response.raise_for_status()
                pdf_path.write_bytes(response.content)
            pdf_paths.append(str(pdf_path))
        except Exception as e:
            print(f"Failed to download {pdf_url}: {e}")
    return pdf_paths

def cleanup_tmp_folder():
    """Deletes the tmp folder and all its contents."""
    if TMP_DIR.exists():
        for f in TMP_DIR.iterdir():
            f.unlink()
        TMP_DIR.rmdir()
