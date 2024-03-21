import { useLoaderData, useNavigate, Form } from "react-router-dom";

export default function CreateProject() {
    const { project } = useLoaderData();
    const navigate = useNavigate();

    return (
        <div id="detail">
            <h1>Create Project</h1>
            <Form method="post" id="contact-form">
                <p>
                    <span>Title</span>
                    <input
                        placeholder="project title"
                        aria-label="project title"
                        type="text"
                        name="title"
                        defaultValue={project.title}
                    />
                </p>
                <p>
                    <button type="submit">Save</button>
                    <button
                        type="button"
                        onClick={() => {
                            navigate(-1);
                        }}
                    >
                        Cancel
                    </button>
                </p>
            </Form>
        </div>
    );
}
