import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getProjects, updateProjectStatus } from './api/client';
import './App.css';

function App() {
  const queryClient = useQueryClient();
  const { data: projects, isLoading, isError } = useQuery({
    queryKey: ['projects'], 
    queryFn: getProjects, 
  });

  // useMutation est un hook pour les opérations qui modifient des données (POST, PATCH, DELETE).
  const { mutate: toggleProjectStatus, isPending: isUpdating } = useMutation({
    mutationFn: ({ projectId, isActive }: { projectId: number; isActive: boolean }) =>
      updateProjectStatus(projectId, isActive),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
    onError: (error) => {
        alert(`Erreur lors de la mise à jour : ${error.message}`);
    }
  });

  // Gestionnaire pour le clic sur le bouton
  const handleToggle = (projectId: number, currentStatus: boolean) => {
    toggleProjectStatus({ projectId, isActive: !currentStatus });
  };

  // Affichage pendant le chargement
  if (isLoading) {
    return <div className="container"><span>Chargement des projets...</span></div>;
  }

  // Affichage en cas d'erreur réseau
  if (isError) {
    return <div className="container"><span>Erreur : Impossible de contacter le serveur backend.</span></div>;
  }

  return (
    <div className="container">
      <h1>Tableau de bord des Projets</h1>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Nom du Projet</th>
              <th>Date de Création</th>
              <th>Statut</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {projects?.map((project) => (
              <tr key={project.id}>
                <td>{project.name}</td>
                <td>{new Date(project.created_at).toLocaleDateString('fr-FR')}</td>
                <td>
                  <span className={`status ${project.is_active ? 'active' : 'inactive'}`}>
                    {project.is_active ? 'Actif' : 'Inactif'}
                  </span>
                </td>
                <td>
                  <button
                    onClick={() => handleToggle(project.id, project.is_active)}
                    disabled={isUpdating}
                  >
                    {project.is_active ? 'Désactiver' : 'Activer'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
