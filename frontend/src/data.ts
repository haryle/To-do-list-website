type ID = number | string;

export interface ProjectDTO {
    id: ID;
    title: string;
    tasks: Array<TaskDTO> 
}

export interface TaskDTO {
    id: ID;
    title: string;
    status: boolean;
    description: string | null;
    deadline: Date | null; 
}

const testTasks = [
    {
        id: 0,
        title: "first_tag",
        status: true,
    },
    {
        id: 1,
        title: "second_tag",
        status: false,
    },
];

const PROJECT_URL = "http://127.0.0.1:8000/project";

export async function getProjects(): Promise<Array<ProjectDTO>> {
    const coroutine = await fetch(PROJECT_URL);
    const result = await coroutine.json();
    return result;
}

export async function getProjectByID(id): Promise<ProjectDTO> {
    const coroutine = await fetch(`${PROJECT_URL}/${id}/tasks`)
    return await coroutine.json();
}

export async function getDefaultProject(): Promise<ProjectDTO>{
    return {id: 0, title: "New Project", tasks: []}
}

export async function createProject(data: ProjectDTO): Promise<ProjectDTO> {
    const coroutine = await fetch(PROJECT_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    const result = await coroutine.json();
    return result;
}

export async function updateProject(id: ID, data: ProjectDTO): Promise<ProjectDTO>{
    const coroutine = await fetch(`${PROJECT_URL}/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    const result = await coroutine.json();
    return result;
}

export async function deleteProject(id: ID){
    const coroutine = await fetch(`${PROJECT_URL}/${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
    });
}