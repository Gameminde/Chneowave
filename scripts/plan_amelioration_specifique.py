#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plan d'amélioration spécifique pour CHNeoWave
Basé sur l'analyse de qualité du code
"""

import json
from pathlib import Path
from typing import Dict, List, Any

class ImprovementPlanner:
    """Générateur de plan d'amélioration spécifique"""
    
    def __init__(self, metrics_file: str):
        self.metrics_file = Path(metrics_file)
        self.metrics = self._load_metrics()
        self.improvements = []
        
    def _load_metrics(self) -> Dict[str, Any]:
        """Charge les métriques depuis le fichier JSON"""
        try:
            with open(self.metrics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur chargement métriques: {e}")
            return {}
    
    def generate_improvement_plan(self) -> List[Dict[str, Any]]:
        """Génère un plan d'amélioration détaillé"""
        print("🎯 Génération du plan d'amélioration spécifique...")
        
        # Analyser les problèmes de complexité
        self._analyze_complexity_issues()
        
        # Analyser les fichiers volumineux
        self._analyze_large_files()
        
        # Recommandations générales
        self._add_general_recommendations()
        
        return self.improvements
    
    def _analyze_complexity_issues(self):
        """Analyse les problèmes de complexité et propose des solutions"""
        complexity_issues = self.metrics.get('complexity_issues', [])
        
        if not complexity_issues:
            return
            
        # Grouper par fichier
        files_with_issues = {}
        for issue in complexity_issues:
            file_path = issue['file']
            if file_path not in files_with_issues:
                files_with_issues[file_path] = []
            files_with_issues[file_path].append(issue)
        
        # Créer des recommandations par fichier
        for file_path, issues in files_with_issues.items():
            total_complexity = sum(issue['complexity'] for issue in issues)
            
            improvement = {
                'type': 'complexity_reduction',
                'priority': 'high' if total_complexity > 50 else 'medium',
                'file': file_path,
                'issues_count': len(issues),
                'total_complexity': total_complexity,
                'functions': [issue['function'] for issue in issues],
                'recommendations': self._get_complexity_recommendations(file_path, issues)
            }
            
            self.improvements.append(improvement)
    
    def _get_complexity_recommendations(self, file_path: str, issues: List[Dict]) -> List[str]:
        """Génère des recommandations spécifiques pour réduire la complexité"""
        recommendations = []
        
        for issue in issues:
            func_name = issue['function']
            complexity = issue['complexity']
            
            if complexity > 20:
                recommendations.append(
                    f"🔴 URGENT - Fonction `{func_name}` (complexité: {complexity}) - "
                    "Diviser en plusieurs fonctions plus petites"
                )
            elif complexity > 15:
                recommendations.append(
                    f"🟡 Fonction `{func_name}` (complexité: {complexity}) - "
                    "Extraire la logique conditionnelle en méthodes séparées"
                )
            else:
                recommendations.append(
                    f"🟢 Fonction `{func_name}` (complexité: {complexity}) - "
                    "Simplifier les conditions ou utiliser des dictionnaires de dispatch"
                )
        
        # Recommandations spécifiques par type de fichier
        if 'view_manager.py' in file_path:
            recommendations.append(
                "💡 Considérer l'utilisation du pattern State pour gérer les transitions de vues"
            )
        elif 'config' in file_path:
            recommendations.append(
                "💡 Utiliser des classes de configuration avec validation automatique (pydantic)"
            )
        elif 'validator' in file_path:
            recommendations.append(
                "💡 Créer des validateurs spécialisés par type de données"
            )
        
        return recommendations
    
    def _analyze_large_files(self):
        """Analyse les fichiers volumineux et propose des refactorisations"""
        large_files = [
            f for f in self.metrics.get('files_by_size', [])
            if f['size_category'] in ['large', 'very_large']
        ]
        
        for file_info in large_files:
            file_path = file_info['file']
            lines = file_info['lines']
            
            improvement = {
                'type': 'file_refactoring',
                'priority': 'high' if lines > 800 else 'medium',
                'file': file_path,
                'lines': lines,
                'recommendations': self._get_refactoring_recommendations(file_path, lines)
            }
            
            self.improvements.append(improvement)
    
    def _get_refactoring_recommendations(self, file_path: str, lines: int) -> List[str]:
        """Génère des recommandations de refactorisation pour les gros fichiers"""
        recommendations = []
        
        if 'material_components.py' in file_path:
            recommendations.extend([
                "🔧 Diviser en modules spécialisés par type de composant (buttons, inputs, dialogs)",
                "🔧 Créer un factory pattern pour la création de composants",
                "🔧 Extraire les styles CSS dans des fichiers séparés"
            ])
        
        elif 'analysis_view.py' in file_path:
            recommendations.extend([
                "🔧 Séparer la logique d'analyse de l'interface utilisateur",
                "🔧 Créer des widgets spécialisés pour chaque type d'analyse",
                "🔧 Utiliser des contrôleurs dédiés pour chaque onglet d'analyse"
            ])
        
        elif 'acquisition_controller.py' in file_path:
            recommendations.extend([
                "🔧 Séparer la logique d'acquisition de la gestion de l'interface",
                "🔧 Créer des classes spécialisées pour chaque type de capteur",
                "🔧 Utiliser des workers asynchrones pour l'acquisition de données"
            ])
        
        elif 'calibration_view.py' in file_path:
            recommendations.extend([
                "🔧 Extraire la logique de génération PDF dans un module séparé",
                "🔧 Créer des widgets réutilisables pour les différents types de calibration",
                "🔧 Séparer la validation des données de l'interface"
            ])
        
        elif 'graph_manager.py' in file_path:
            recommendations.extend([
                "🔧 Créer des classes spécialisées pour chaque type de graphique",
                "🔧 Utiliser des factories pour la création de graphiques",
                "🔧 Séparer la logique de rendu de la gestion des données"
            ])
        
        else:
            # Recommandations génériques
            if lines > 1000:
                recommendations.append("🔧 URGENT - Diviser ce fichier en au moins 3 modules distincts")
            elif lines > 600:
                recommendations.append("🔧 Diviser ce fichier en 2 modules avec des responsabilités claires")
            else:
                recommendations.append("🔧 Extraire les classes/fonctions utilitaires dans des modules séparés")
        
        return recommendations
    
    def _add_general_recommendations(self):
        """Ajoute des recommandations générales basées sur les métriques"""
        # Recommandations basées sur les métriques globales
        comment_ratio = (self.metrics.get('comment_lines', 0) / 
                        max(self.metrics.get('code_lines', 1), 1)) * 100
        
        if comment_ratio < 10:
            self.improvements.append({
                'type': 'documentation',
                'priority': 'medium',
                'description': 'Améliorer la documentation du code',
                'current_ratio': f"{comment_ratio:.1f}%",
                'target_ratio': '15-20%',
                'recommendations': [
                    "📝 Ajouter des commentaires explicatifs dans les fonctions complexes",
                    "📝 Documenter les algorithmes et les formules utilisées",
                    "📝 Ajouter des exemples d'utilisation dans les docstrings"
                ]
            })
        
        # Recommandations sur l'architecture
        self.improvements.append({
            'type': 'architecture',
            'priority': 'low',
            'description': 'Améliorations architecturales',
            'recommendations': [
                "🏗️ Implémenter des interfaces (ABC) pour les composants critiques",
                "🏗️ Ajouter un système de plugins pour les backends d'acquisition",
                "🏗️ Créer un système de cache pour les résultats d'analyse",
                "🏗️ Implémenter un système de configuration par environnement"
            ]
        })
        
        # Recommandations sur les tests
        test_coverage = self.metrics.get('test_coverage_estimate', 0)
        if test_coverage < 80:  # Bien que l'estimation soit à 100%, c'est probablement surestimé
            self.improvements.append({
                'type': 'testing',
                'priority': 'high',
                'description': 'Améliorer la couverture de tests réelle',
                'recommendations': [
                    "🧪 Ajouter des tests d'intégration pour le workflow complet",
                    "🧪 Créer des tests de performance pour l'acquisition de données",
                    "🧪 Ajouter des tests de régression pour l'interface utilisateur",
                    "🧪 Implémenter des tests de charge pour les gros datasets"
                ]
            })
    
    def generate_action_plan(self) -> str:
        """Génère un plan d'action détaillé"""
        plan = []
        plan.append("# 🎯 Plan d'Action Spécifique - CHNeoWave")
        plan.append(f"**Basé sur l'analyse de {self.metrics.get('files_analyzed', 0)} fichiers**")
        plan.append("")
        
        # Grouper par priorité
        high_priority = [i for i in self.improvements if i.get('priority') == 'high']
        medium_priority = [i for i in self.improvements if i.get('priority') == 'medium']
        low_priority = [i for i in self.improvements if i.get('priority') == 'low']
        
        # Actions prioritaires
        if high_priority:
            plan.append("## 🔴 Actions Prioritaires (À faire immédiatement)")
            for i, improvement in enumerate(high_priority, 1):
                plan.append(f"### {i}. {improvement.get('description', improvement['type'].title())}")
                if 'file' in improvement:
                    plan.append(f"**Fichier:** `{improvement['file']}`")
                if 'lines' in improvement:
                    plan.append(f"**Taille:** {improvement['lines']} lignes")
                if 'total_complexity' in improvement:
                    plan.append(f"**Complexité totale:** {improvement['total_complexity']}")
                
                plan.append("**Actions:**")
                for rec in improvement.get('recommendations', []):
                    plan.append(f"- {rec}")
                plan.append("")
        
        # Actions moyennes
        if medium_priority:
            plan.append("## 🟡 Actions Moyennes (À planifier)")
            for i, improvement in enumerate(medium_priority, 1):
                plan.append(f"### {i}. {improvement.get('description', improvement['type'].title())}")
                if 'file' in improvement:
                    plan.append(f"**Fichier:** `{improvement['file']}`")
                
                plan.append("**Actions:**")
                for rec in improvement.get('recommendations', [])[:3]:  # Limiter à 3
                    plan.append(f"- {rec}")
                plan.append("")
        
        # Actions à long terme
        if low_priority:
            plan.append("## 🟢 Améliorations à Long Terme")
            for improvement in low_priority:
                plan.append(f"### {improvement.get('description', improvement['type'].title())}")
                for rec in improvement.get('recommendations', [])[:2]:  # Limiter à 2
                    plan.append(f"- {rec}")
                plan.append("")
        
        # Calendrier suggéré
        plan.append("## 📅 Calendrier Suggéré")
        plan.append("")
        plan.append("### Semaine 1-2: Actions Prioritaires")
        plan.append("- Refactoriser les fonctions les plus complexes")
        plan.append("- Diviser les fichiers les plus volumineux")
        plan.append("- Ajouter des tests critiques")
        plan.append("")
        plan.append("### Semaine 3-4: Actions Moyennes")
        plan.append("- Améliorer la documentation")
        plan.append("- Optimiser les performances")
        plan.append("- Refactoriser les modules moyens")
        plan.append("")
        plan.append("### Mois 2: Améliorations Long Terme")
        plan.append("- Améliorations architecturales")
        plan.append("- Système de plugins")
        plan.append("- Optimisations avancées")
        plan.append("")
        
        plan.append("---")
        plan.append("*Plan généré automatiquement par l'Analyseur CHNeoWave*")
        
        return "\n".join(plan)

def main():
    """Point d'entrée principal"""
    project_root = Path(__file__).parent
    metrics_file = project_root / "metriques_qualite.json"
    
    if not metrics_file.exists():
        print("❌ Fichier de métriques non trouvé. Exécutez d'abord analyse_qualite_code.py")
        return 1
    
    print("🎯 Génération du plan d'amélioration spécifique...")
    
    planner = ImprovementPlanner(str(metrics_file))
    improvements = planner.generate_improvement_plan()
    
    # Générer le plan d'action
    action_plan = planner.generate_action_plan()
    
    # Sauvegarder le plan
    plan_file = project_root / "PLAN_ACTION_SPECIFIQUE.md"
    with open(plan_file, 'w', encoding='utf-8') as f:
        f.write(action_plan)
    
    # Sauvegarder les améliorations détaillées
    improvements_file = project_root / "ameliorations_detaillees.json"
    with open(improvements_file, 'w', encoding='utf-8') as f:
        json.dump(improvements, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Plan d'action généré!")
    print(f"📄 Plan sauvegardé: {plan_file}")
    print(f"📊 Détails sauvegardés: {improvements_file}")
    print()
    print("📋 Résumé des améliorations:")
    
    high_count = len([i for i in improvements if i.get('priority') == 'high'])
    medium_count = len([i for i in improvements if i.get('priority') == 'medium'])
    low_count = len([i for i in improvements if i.get('priority') == 'low'])
    
    print(f"   - 🔴 {high_count} actions prioritaires")
    print(f"   - 🟡 {medium_count} actions moyennes")
    print(f"   - 🟢 {low_count} améliorations long terme")
    print(f"   - 📊 Total: {len(improvements)} recommandations")

if __name__ == "__main__":
    main()