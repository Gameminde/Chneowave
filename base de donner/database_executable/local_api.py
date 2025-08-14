#!/usr/bin/env python3
"""
API Locale SQLite pour la Base de Données d'Instrumentation Maritime
Version simplifiée pour usage local sans serveur PostgreSQL
"""

import sqlite3
import json
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import os

class LocalDatabaseAPI:
    def __init__(self, db_file="instrumentation_maritime.db"):
        self.db_file = db_file
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Vérifier que la base de données existe"""
        if not os.path.exists(self.db_file):
            print(f"❌ Base de données non trouvée: {self.db_file}")
            print("🔧 Exécutez d'abord: python create_local_database.py")
            return False
        return True
    
    def get_connection(self):
        """Obtenir une connexion à la base de données"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        return conn
    
    # =============================================================================
    # STATISTIQUES DASHBOARD
    # =============================================================================
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Obtenir les statistiques pour le dashboard"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Total équipements
            cursor.execute("SELECT COUNT(*) FROM equipements WHERE etat NOT IN ('REBUT', 'REFORME')")
            total_equipements = cursor.fetchone()[0]
            
            # Équipements OK
            cursor.execute("SELECT COUNT(*) FROM equipements WHERE etat = 'OK'")
            equipements_ok = cursor.fetchone()[0]
            
            # Équipements en panne
            cursor.execute("SELECT COUNT(*) FROM equipements WHERE etat = 'EN_PANNE'")
            equipements_panne = cursor.fetchone()[0]
            
            # Vérifications expirées
            cursor.execute("SELECT COUNT(*) FROM equipements WHERE prochaine_verification < date('now')")
            verifications_expirees = cursor.fetchone()[0]
            
            # Interventions du mois
            cursor.execute("""
                SELECT COUNT(*) FROM interventions 
                WHERE date_intervention >= date('now', 'start of month')
            """)
            interventions_mois = cursor.fetchone()[0]
            
            # Coût maintenance année
            cursor.execute("""
                SELECT COALESCE(SUM(cout), 0) FROM interventions 
                WHERE strftime('%Y', date_intervention) = strftime('%Y', 'now')
            """)
            cout_maintenance_annee = cursor.fetchone()[0]
            
            # Projets actifs
            cursor.execute("SELECT COUNT(*) FROM projets WHERE statut = 'ACTIF'")
            projets_actifs = cursor.fetchone()[0]
            
            # Licences expirant bientôt
            cursor.execute("""
                SELECT COUNT(*) FROM licences 
                WHERE date_expiration < date('now', '+60 days') AND statut = 'ACTIVE'
            """)
            licences_expire_bientot = cursor.fetchone()[0]
            
            return {
                "total_equipements": total_equipements,
                "equipements_ok": equipements_ok,
                "equipements_panne": equipements_panne,
                "verifications_expirees": verifications_expirees,
                "interventions_mois": interventions_mois,
                "cout_maintenance_annee": float(cout_maintenance_annee),
                "projets_actifs": projets_actifs,
                "licences_expire_bientot": licences_expire_bientot
            }
        
        finally:
            conn.close()
    
    def get_alertes_metrologie(self) -> List[Dict[str, Any]]:
        """Obtenir les alertes métrologiques"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    e.id_equipement,
                    e.numero,
                    e.description,
                    s.nom as service,
                    e.prochaine_verification,
                    CASE 
                        WHEN e.prochaine_verification < date('now') THEN 'EXPIRE'
                        WHEN e.prochaine_verification < date('now', '+30 days') THEN 'ALERTE'
                        WHEN e.prochaine_verification < date('now', '+60 days') THEN 'ATTENTION'
                        ELSE 'OK'
                    END as statut_alerte,
                    julianday('now') - julianday(e.prochaine_verification) as jours_retard
                FROM equipements e
                LEFT JOIN services s ON e.service_id = s.id
                WHERE e.prochaine_verification IS NOT NULL
                    AND e.etat NOT IN ('REBUT', 'REFORME')
                    AND e.prochaine_verification < date('now', '+60 days')
                ORDER BY e.prochaine_verification
            """)
            
            alertes = []
            for row in cursor.fetchall():
                alertes.append({
                    "id_equipement": row["id_equipement"],
                    "numero": row["numero"],
                    "description": row["description"],
                    "service": row["service"],
                    "prochaine_verification": row["prochaine_verification"],
                    "statut_alerte": row["statut_alerte"],
                    "jours_retard": int(row["jours_retard"]) if row["jours_retard"] > 0 else None
                })
            
            return alertes
        
        finally:
            conn.close()
    
    def get_kpi_services(self) -> List[Dict[str, Any]]:
        """Obtenir les KPI par service"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    s.id as service_id,
                    s.code,
                    s.nom as service,
                    COUNT(e.id_equipement) as total_equipements,
                    SUM(CASE WHEN e.etat = 'OK' THEN 1 ELSE 0 END) as equipements_ok,
                    SUM(CASE WHEN e.etat = 'EN_PANNE' THEN 1 ELSE 0 END) as equipements_panne,
                    SUM(CASE WHEN e.etat = 'MAINTENANCE' THEN 1 ELSE 0 END) as equipements_maintenance,
                    ROUND(
                        CAST(SUM(CASE WHEN e.etat = 'OK' THEN 1 ELSE 0 END) AS FLOAT) / 
                        NULLIF(COUNT(e.id_equipement), 0) * 100, 2
                    ) as taux_disponibilite,
                    SUM(CASE WHEN e.prochaine_verification < date('now') THEN 1 ELSE 0 END) as verifications_expirees
                FROM services s
                LEFT JOIN equipements e ON s.id = e.service_id
                WHERE e.etat IS NULL OR e.etat NOT IN ('REBUT', 'REFORME')
                GROUP BY s.id, s.code, s.nom
                ORDER BY s.nom
            """)
            
            kpis = []
            for row in cursor.fetchall():
                kpis.append({
                    "service_id": row["service_id"],
                    "code": row["code"],
                    "service": row["service"],
                    "total_equipements": row["total_equipements"],
                    "equipements_ok": row["equipements_ok"],
                    "equipements_panne": row["equipements_panne"],
                    "equipements_maintenance": row["equipements_maintenance"],
                    "taux_disponibilite": float(row["taux_disponibilite"] or 0),
                    "verifications_expirees": row["verifications_expirees"]
                })
            
            return kpis
        
        finally:
            conn.close()
    
    # =============================================================================
    # GESTION DES ÉQUIPEMENTS
    # =============================================================================
    
    def get_services(self) -> List[Dict[str, Any]]:
        """Obtenir tous les services"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM services ORDER BY nom")
            services = []
            for row in cursor.fetchall():
                services.append({
                    "id": row["id"],
                    "code": row["code"],
                    "nom": row["nom"],
                    "responsable": row["responsable"],
                    "description": row["description"]
                })
            return services
        
        finally:
            conn.close()
    
    def get_equipements(self, service_id: Optional[int] = None, 
                       etat: Optional[str] = None,
                       search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtenir les équipements avec filtres"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Construction de la requête avec filtres
            query = """
                SELECT 
                    e.*,
                    s.nom as service_nom,
                    s.code as service_code
                FROM equipements e
                LEFT JOIN services s ON e.service_id = s.id
                WHERE 1=1
            """
            params = []
            
            if service_id:
                query += " AND e.service_id = ?"
                params.append(service_id)
            
            if etat:
                query += " AND e.etat = ?"
                params.append(etat)
            
            if search:
                query += " AND (e.description LIKE ? OR e.marque_type LIKE ? OR e.numero LIKE ?)"
                search_param = f"%{search}%"
                params.extend([search_param, search_param, search_param])
            
            query += " ORDER BY e.numero"
            
            cursor.execute(query, params)
            
            equipements = []
            for row in cursor.fetchall():
                equipement = {
                    "id_equipement": row["id_equipement"],
                    "numero": row["numero"],
                    "description": row["description"],
                    "marque_type": row["marque_type"],
                    "numero_serie": row["numero_serie"],
                    "n_inventaire": row["n_inventaire"],
                    "utilisateur": row["utilisateur"],
                    "localisation": row["localisation"],
                    "etat": row["etat"],
                    "annee_acquisition": row["annee_acquisition"],
                    "valeur_acquisition": float(row["valeur_acquisition"]) if row["valeur_acquisition"] else None,
                    "statut_metrologique": row["statut_metrologique"],
                    "date_derniere_verification": row["date_derniere_verification"],
                    "prochaine_verification": row["prochaine_verification"],
                    "frequence_verification_mois": row["frequence_verification_mois"],
                    "criticite": row["criticite"],
                    "commentaires": row["commentaires"],
                    "service": {
                        "id": row["service_id"],
                        "nom": row["service_nom"],
                        "code": row["service_code"]
                    } if row["service_id"] else None
                }
                equipements.append(equipement)
            
            return equipements
        
        finally:
            conn.close()
    
    def get_equipement(self, equipement_id: int) -> Optional[Dict[str, Any]]:
        """Obtenir un équipement par ID"""
        equipements = self.get_equipements()
        for eq in equipements:
            if eq["id_equipement"] == equipement_id:
                return eq
        return None
    
    # =============================================================================
    # RECHERCHE
    # =============================================================================
    
    def search_equipements(self, search_term: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Recherche full-text dans les équipements"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    e.*,
                    s.nom as service_nom,
                    s.code as service_code,
                    (CASE 
                        WHEN e.numero LIKE ? THEN 10
                        WHEN e.n_inventaire LIKE ? THEN 8
                        WHEN e.description LIKE ? THEN 5
                        WHEN e.marque_type LIKE ? THEN 3
                        ELSE 1
                    END) as search_score
                FROM equipements e
                LEFT JOIN services s ON e.service_id = s.id
                WHERE e.numero LIKE ? 
                   OR e.description LIKE ? 
                   OR e.marque_type LIKE ? 
                   OR e.n_inventaire LIKE ?
                ORDER BY search_score DESC, e.numero
                LIMIT ?
            """, [f"%{search_term}%"] * 8 + [limit])
            
            results = []
            for row in cursor.fetchall():
                result = {
                    "id_equipement": row["id_equipement"],
                    "numero": row["numero"],
                    "description": row["description"],
                    "marque_type": row["marque_type"],
                    "service_nom": row["service_nom"],
                    "search_score": row["search_score"]
                }
                results.append(result)
            
            return results
        
        finally:
            conn.close()
    
    # =============================================================================
    # EXPORT
    # =============================================================================
    
    def export_equipements(self, format_type: str = "json") -> Dict[str, Any]:
        """Export des équipements"""
        equipements = self.get_equipements()
        
        if format_type == "json":
            return {
                "data": equipements,
                "count": len(equipements),
                "export_date": datetime.now().isoformat()
            }
        
        elif format_type == "csv":
            csv_content = "ID,Numero,Description,Marque,Service,Etat,Statut_Metrologique,Prochaine_Verification\n"
            for eq in equipements:
                service_nom = eq["service"]["nom"] if eq["service"] else "N/A"
                csv_content += f"{eq['id_equipement']},{eq['numero']},{eq['description']},{eq['marque_type'] or 'N/A'},{service_nom},{eq['etat']},{eq['statut_metrologique']},{eq['prochaine_verification'] or 'N/A'}\n"
            
            return {"csv_data": csv_content}
        
        return {"error": "Format non supporté"}

# =============================================================================
# SERVEUR WEB SIMPLE
# =============================================================================

def create_simple_web_server():
    """Créer un serveur web simple pour l'API locale"""
    
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    import json
    
    # Instance de l'API
    api = LocalDatabaseAPI()
    
    class LocalAPIHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            """Gérer les requêtes GET"""
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)
            
            # Headers CORS
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            try:
                if path == '/api/dashboard/stats':
                    data = api.get_dashboard_stats()
                
                elif path == '/api/dashboard/alertes-metrologie':
                    data = api.get_alertes_metrologie()
                
                elif path == '/api/dashboard/kpi-services':
                    data = api.get_kpi_services()
                
                elif path == '/api/services':
                    data = api.get_services()
                
                elif path == '/api/equipements':
                    service_id = int(query_params.get('service_id', [None])[0]) if query_params.get('service_id', [None])[0] else None
                    etat = query_params.get('etat', [None])[0]
                    search = query_params.get('search', [None])[0]
                    data = api.get_equipements(service_id, etat, search)
                
                elif path.startswith('/api/equipements/'):
                    equipement_id = int(path.split('/')[-1])
                    data = api.get_equipement(equipement_id)
                    if not data:
                        self.send_error(404, "Équipement non trouvé")
                        return
                
                elif path == '/api/search/equipements':
                    search_term = query_params.get('q', [''])[0]
                    limit = int(query_params.get('limit', [20])[0])
                    data = api.search_equipements(search_term, limit)
                
                elif path == '/api/export/equipements':
                    format_type = query_params.get('format', ['json'])[0]
                    data = api.export_equipements(format_type)
                
                elif path == '/health':
                    data = {
                        "status": "healthy",
                        "timestamp": datetime.now().isoformat(),
                        "database": "connected"
                    }
                
                else:
                    data = {
                        "message": "API Locale Instrumentation Maritime",
                        "version": "1.0.0",
                        "status": "active",
                        "endpoints": [
                            "/api/dashboard/stats",
                            "/api/dashboard/alertes-metrologie",
                            "/api/dashboard/kpi-services",
                            "/api/services",
                            "/api/equipements",
                            "/api/search/equipements",
                            "/api/export/equipements",
                            "/health"
                        ]
                    }
                
                # Envoyer la réponse JSON
                response = json.dumps(data, ensure_ascii=False, default=str)
                self.wfile.write(response.encode('utf-8'))
            
            except Exception as e:
                error_response = {"error": str(e)}
                response = json.dumps(error_response)
                self.wfile.write(response.encode('utf-8'))
        
        def do_OPTIONS(self):
            """Gérer les requêtes OPTIONS pour CORS"""
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
        
        def log_message(self, format, *args):
            """Personnaliser les logs"""
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")
    
    return HTTPServer, LocalAPIHandler

if __name__ == "__main__":
    print("🚀 Démarrage de l'API Locale d'Instrumentation Maritime")
    print("=" * 60)
    
    # Vérifier la base de données
    api = LocalDatabaseAPI()
    if not api.ensure_database_exists():
        exit(1)
    
    # Test rapide
    print("🔍 Test de la base de données...")
    stats = api.get_dashboard_stats()
    print(f"✅ {stats['total_equipements']} équipements trouvés")
    
    # Démarrer le serveur web
    HTTPServer, LocalAPIHandler = create_simple_web_server()
    
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, LocalAPIHandler)
    
    print(f"\n🌐 Serveur API démarré sur http://localhost:8000")
    print(f"📊 Dashboard: http://localhost:8000")
    print(f"📖 API Endpoints: http://localhost:8000/health")
    print(f"\n⏹️  Appuyez sur Ctrl+C pour arrêter")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 Serveur arrêté")
        httpd.shutdown()
