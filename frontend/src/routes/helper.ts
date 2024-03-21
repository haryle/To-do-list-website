import {
    createProject,
    getDefaultProject,
    getProjectByID,
    getProjects,
    ProjectDTO,
    updateProject,
    TaskDTO,
    deleteProject,
} from "../data";
import { redirect } from "react-router-dom";

export async function loaderProject(): Promise<Array<ProjectDTO>> {
    const projects = await getProjects();
    return projects;
}

export async function loaderProjectId({ params }) {
    const project = await getProjectByID(params.projectId);
    return { project };
}

export async function loaderDefaultProject() {
    const project = await getDefaultProject();
    return { project };
}

export async function actionCreateProject({ request, params }) { 
    const formData = await request.formData();
    const data = <ProjectDTO> Object.fromEntries(formData);
    const ret_result = await createProject(data);
    return redirect(`/project/${ret_result.id}`);
}

export async function actionUpdateProject({request, params}){
    const formData = await request.formData();
    const data = <ProjectDTO> Object.fromEntries(formData);
    console.log(data)
    await updateProject(params.projectId, data);
    return redirect(`/project/${params.projectId}`)
}

export async function actionDeleteProject({params}){
    await deleteProject(params.projectId);
    return redirect("/");
}