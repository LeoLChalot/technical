import type { Project } from '../types/entities';

// L'URL de base de notre API backend que nous avons développée
const API_BASE_URL = 'http://127.0.0.1:8000/api';
const API_TOKEN = 'entropy';

/**
 * Récupère la liste de tous les projets depuis le backend.
 */
export const getProjects = async (): Promise<Project[]> => {
  // --- EDIT: Ajout du paramètre token=entropy ---
  const response = await fetch(`${API_BASE_URL}/projects/?token=${API_TOKEN}`);
  if (!response.ok) {
    throw new Error('La récupération des projets a échoué.');
  }
  return response.json();
};

/**
 * Met à jour le statut (actif/inactif) d'un projet.
 * @param projectId - L'ID du projet à mettre à jour.
 * @param isActive - Le nouveau statut du projet.
 */
export const updateProjectStatus = async (
  projectId: number,
  isActive: boolean
): Promise<Project> => {
  // --- EDIT: Ajout du paramètre token=entropy ---
  const response = await fetch(`${API_BASE_URL}/projects/${projectId}?token=${API_TOKEN}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ is_active: isActive }),
  });

  if (!response.ok) {
    throw new Error("La mise à jour du statut du projet a échoué.");
  }
  return response.json();
};