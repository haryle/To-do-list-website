type ID = number | string 

export interface ProjectDTO{
    id: ID
    title: string 
}

export interface TaskDTO{
    id: ID
    title: string 
    status: boolean 
}

const testTasks = [
    {
        id: 0, title: "first_tag", status: true
    },
    {
        id: 1, title: "second_tag", status: false 
    }
];

const PROJECT_URL = "http://127.0.0.1:8000/project"

export async function getProjects(): Promise<Array<ProjectDTO>>{
    const coroutine = await fetch(PROJECT_URL);
    const result = await coroutine.json()
    console.log(result);
    return result;
};

export async function getTasks(): Promise<Array<TaskDTO>>{
    return testTasks;
}