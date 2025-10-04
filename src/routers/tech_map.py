"""
AI Cyber Tool - Tech Map Router
API ендпоінти для технічної карти та специфікацій
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from loguru import logger
from ..core.config import get_settings

router = APIRouter()
settings = get_settings()
templates = Jinja2Templates(directory="templates")


@router.get("/tech-map", response_class=HTMLResponse)
async def tech_map_page(request: Request, lang: str = "uk"):
    """Сторінка технічної карти"""
    try:
        # Читаємо технічну карту
        tech_map_path = Path(f"architecture/{lang}/technical_map.md")
        if not tech_map_path.exists():
            tech_map_path = Path("architecture/uk/technical_map.md")
        
        with open(tech_map_path, "r", encoding="utf-8") as f:
            tech_map_content = f.read()
        
        # Отримуємо список діаграм
        diagrams = []
        architecture_dir = Path("architecture")
        
        # Знайти всі PNG файли
        for png_file in architecture_dir.glob("*.png"):
            svg_file = png_file.with_suffix('.svg')
            mmd_file = png_file.with_suffix('.mmd')
            
            diagrams.append({
                "name": png_file.stem,
                "png_path": f"/architecture/{png_file.name}",
                "svg_path": f"/architecture/{svg_file.name}" if svg_file.exists() else None,
                "mmd_path": f"/architecture/{mmd_file.name}" if mmd_file.exists() else None
            })
        
        return templates.TemplateResponse("tech_map.html", {
            "request": request,
            "tech_map_content": tech_map_content,
            "diagrams": diagrams,
            "lang": lang
        })
        
    except Exception as e:
        logger.error(f"Failed to load tech map: {e}")
        raise HTTPException(status_code=500, detail="Failed to load technical map")


@router.get("/tech-map/api")
async def tech_map_api():
    """API для отримання інформації про технічну карту"""
    try:
        diagrams = []
        architecture_dir = Path("architecture")
        
        # Знайти всі PNG файли
        for png_file in architecture_dir.glob("*.png"):
            svg_file = png_file.with_suffix('.svg')
            mmd_file = png_file.with_suffix('.mmd')
            
            diagrams.append({
                "name": png_file.stem,
                "png_path": f"/architecture/{png_file.name}",
                "svg_path": f"/architecture/{svg_file.name}" if svg_file.exists() else None,
                "mmd_path": f"/architecture/{mmd_file.name}" if mmd_file.exists() else None,
                "size": png_file.stat().st_size,
                "modified": png_file.stat().st_mtime
            })
        
        return {
            "diagrams": diagrams,
            "count": len(diagrams),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Failed to get tech map API: {e}")
        raise HTTPException(status_code=500, detail="Failed to get tech map data")


@router.get("/specs", response_class=HTMLResponse)
async def specs_page(request: Request, lang: str = "uk"):
    """Сторінка специфікацій сервісів"""
    try:
        # Читаємо README з папки specs
        specs_readme_path = Path("specs/README.md")
        if specs_readme_path.exists():
            with open(specs_readme_path, "r", encoding="utf-8") as f:
                specs_content = f.read()
        else:
            specs_content = "# Специфікації сервісів\n\nСпецифікації будуть доступні після створення."
        
        # Отримуємо список специфікацій
        specs_files = []
        specs_dir = Path("specs")
        if specs_dir.exists():
            for file_path in specs_dir.glob("*.md"):
                if file_path.name != "README.md":
                    specs_files.append({
                        "name": file_path.stem,
                        "title": file_path.stem.replace("_", " ").title(),
                        "path": f"/specs/{file_path.name}"
                    })
        
        return templates.TemplateResponse("specs.html", {
            "request": request,
            "lang": lang,
            "specs_content": specs_content,
            "specs_files": specs_files,
            "version": settings.api_version,
            "status": "running"
        })
    except Exception as e:
        logger.error(f"Error loading specs page: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load specs page: {str(e)}")


@router.get("/specs/{spec_name}", response_class=HTMLResponse)
async def spec_detail(request: Request, spec_name: str, lang: str = "uk"):
    """Детальна сторінка специфікації"""
    try:
        spec_path = Path(f"specs/{spec_name}.md")
        if not spec_path.exists():
            raise HTTPException(status_code=404, detail="Specification not found")
        
        with open(spec_path, "r", encoding="utf-8") as f:
            spec_content = f.read()
        
        # Отримуємо список всіх специфікацій для навігації
        specs_files = []
        specs_dir = Path("specs")
        if specs_dir.exists():
            for file_path in specs_dir.glob("*.md"):
                if file_path.name != "README.md":
                    specs_files.append({
                        "name": file_path.stem,
                        "title": file_path.stem.replace("_", " ").title(),
                        "path": f"/specs/{file_path.name}",
                        "active": file_path.stem == spec_name
                    })
        
        return templates.TemplateResponse("spec_detail.html", {
            "request": request,
            "lang": lang,
            "spec_name": spec_name,
            "spec_title": spec_name.replace("_", " ").title(),
            "spec_content": spec_content,
            "specs_files": specs_files,
            "version": settings.api_version,
            "status": "running"
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading spec {spec_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load specification: {str(e)}")


@router.get("/api/specs")
async def get_specs_list():
    """API для отримання списку специфікацій"""
    try:
        specs_files = []
        specs_dir = Path("specs")
        if specs_dir.exists():
            for file_path in specs_dir.glob("*.md"):
                specs_files.append({
                    "name": file_path.stem,
                    "title": file_path.stem.replace("_", " ").title(),
                    "path": f"/specs/{file_path.name}",
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime
                })
        
        return {
            "specs": specs_files,
            "count": len(specs_files),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error getting specs list: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get specs list: {str(e)}")
