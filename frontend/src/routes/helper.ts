import { getProjects, ProjectDTO, TaskDTO} from "../data";

export async function loaderProject(): Promise<Array<ProjectDTO>> {
    const projects = await getProjects();
    return projects;
}
