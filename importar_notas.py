"""Importa solo los promedios finales. Los datos privados nunca van a static/."""
from pathlib import Path
import json
import re
import unicodedata
from datetime import datetime, timezone
import xlrd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent

def normalized(value):
    value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode()
    return ' '.join(re.findall(r'[A-Z0-9]+', value.upper()))

def importar():
    workbook = load_workbook(ROOT.parent.parent / 'Registro_Calificaciones_Paralelo_I.xlsx', data_only=True)
    roster = {}
    for row in workbook['1ro I Matemática'].iter_rows(min_row=7, values_only=True):
        if not isinstance(row[0], (int, float)) or not row[1] or not row[3]:
            continue
        cedula = str(row[3]).strip()
        if cedula.endswith('.0'):
            cedula = cedula[:-2]
        if cedula.isdigit():
            cedula = cedula.zfill(10)
        key = normalized(row[1])
        if key in roster or any(s['cedula'] == cedula for s in roster.values()):
            raise ValueError('Nombre o cédula duplicados: revisar padrón.')
        roster[key] = {'cedula': cedula, 'nombre': ' '.join(row[1].split()), 'notas': {}}
    subjects = [
        ('matematica', '1.I Matematica.xls', 'Matemática', '📐'),
        ('lengua', '1ro. LENGUA Y LITERATURA.xls', 'Lengua y Literatura', '📚'),
        ('fisica', '1.I Fisica.xls', 'Física', '⚛️'),
        ('quimica', '1.I-QUÍMICA.xls', 'Química', '🧪'),
        ('biologia', '1.I-BIOLOGÍA.xls', 'Biología', '🧬'),
        ('historia', '1.I. Historia.xls', 'Historia', '🏛️'),
        ('filosofia', '1.I. Filosofía.xls', 'Filosofía', '💡'),
        ('ingles', '1.I Inglés.xls', 'Inglés', '🌎'),
        ('ciudadania', '1.I Educación Ciudadanía.xls', 'Educación para la Ciudadanía', '🤝'),
        ('civica', '1.I Civica.xls', 'Cívica', '🇪🇨'),
        ('eca', '1.I - ECA.xls', 'Educación Cultural y Artística', '🎨'),
        ('educacion-fisica', '1.I - Educ. Fisica.xls', 'Educación Física', '⚽'),
        ('emprendimiento', '1.I - Emprendimiento.xls', 'Emprendimiento y Gestión', '🚀'),
    ]
    audit = []
    for sid, filename, label, emoji in subjects:
        sheet = xlrd.open_workbook(ROOT.parent / filename).sheet_by_index(0)
        count = 0
        seen = set()
        for i in range(12, sheet.nrows):
            row = sheet.row_values(i)
            if not isinstance(row[0], (int, float)) or not isinstance(row[1], (int, float)) or not row[2]:
                continue
            key = normalized(row[2])
            if key not in roster:
                raise ValueError(f'Estudiante sin cédula en el padrón: {row[2]} ({filename})')
            if key in seen:
                raise ValueError(f'Estudiante duplicado en {filename}')
            seen.add(key)
            cell = sheet.cell(i, 14)
            grade = round(cell.value, 2) if cell.ctype == xlrd.XL_CELL_NUMBER else None
            if grade is not None and not 0 <= grade <= 10:
                raise ValueError(f'Nota fuera de rango: {filename}, fila {i+1}')
            roster[key]['notas'][sid] = grade
            count += grade is not None
        audit.append({'archivo': filename, 'asignatura': label, 'estudiantes': len(seen), 'con_nota_final': count})
    output = {
        'actualizado': datetime.now(timezone.utc).isoformat(),
        'periodo': 'Agosto 2026 – Enero 2027',
        'asignaturas': [{'id': sid, 'nombre': label, 'emoji': emoji} for sid, _, label, emoji in subjects],
        'estudiantes': {s['cedula']: s for s in roster.values()},
    }
    private = ROOT / 'datos'
    private.mkdir(exist_ok=True)
    (private / 'calificaciones.json').write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    (private / 'informe_importacion.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Importados {len(roster)} estudiantes y {len(subjects)} asignaturas.')
    print(json.dumps(audit, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    importar()
