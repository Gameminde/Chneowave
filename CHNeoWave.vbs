' CHNeoWave - Raccourci de lancement
' Logiciel d'étude maritime - Modèles réduits
' Laboratoire Méditerranéen - Bassins et canaux

Dim objShell, objFSO, scriptDir, batFile

' Obtenir le répertoire du script
Set objFSO = CreateObject("Scripting.FileSystemObject")
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
batFile = scriptDir & "\launch_chneowave.bat"

' Vérifier que le fichier batch existe
If objFSO.FileExists(batFile) Then
    ' Lancer le fichier batch
    Set objShell = CreateObject("WScript.Shell")
    objShell.Run """" & batFile & """", 1, False
Else
    ' Afficher une erreur si le fichier n'existe pas
    MsgBox "Erreur: Fichier de lancement non trouvé!" & vbCrLf & _
           "Chemin attendu: " & batFile, vbCritical, "CHNeoWave - Erreur"
End If

' Nettoyer les objets
Set objShell = Nothing
Set objFSO = Nothing