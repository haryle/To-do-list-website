
const testProjects = [
    {
        id: 0, title: "first_project"
    },
    {
        id: 1, title: "second_project"
    }
];

const testTags = [
    {
        id: 0, title: "first_tag"
    },
    {
        id: 1, title: "second_tag"
    }
];

export async function getProjects(){
    return testProjects;
};

export async function getTags(){
    return testTags;
}