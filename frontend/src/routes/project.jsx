import { useLoaderData, NavLink, Form } from "react-router-dom";
import { useState } from "react";

// eslint-disable-next-line react/prop-types
function ProjecTitleDiv({ project }) {
    // eslint-disable-next-line react/prop-types
    const title = project.title;
    const [isShowing, setIsShowing] = useState(true);

    return (
        <div className="project-title">
            {/* Title */}
            <Form id="project-form" method="post" action="update" className="title">
                <h1 style={{ display: isShowing ? "block" : "none" }}>{title}</h1>
                <input type="text" name="title" placeholder={title} style={{ display: !isShowing ? "block" : "none" }} />
            </Form>

            <div className="buttons">
                {/* Edit Button */}
                <button form="project-form" onClick={() => setIsShowing(!isShowing)} style={{ display: !isShowing ? "block" : "none" }}>Edit</button>
                <button onClick={() => setIsShowing(!isShowing)} style={{ display: isShowing ? "block" : "none" }}>Edit</button>

                {/* Delete Button */}
                <Form
                    method="post"
                    action="delete"
                    onSubmit={(event) => {
                        if (!confirm("Please confirm you want to delete the project")) {
                            event.preventDefault();
                        }
                    }}
                >
                    <button type="submit">Delete</button>
                </Form>
            </div>
        </div>
    );
}

export default function ProjectPage() {
    const { project } = useLoaderData();
    return (
        <div id="detail">
            <ProjecTitleDiv project={project} />

            <h2>Tasks</h2>
            {project.tasks.length ? (
                <nav id="task-nav-content">
                    {project.tasks.map((task) => (
                        <div key={task.id}>
                            <input
                                type="checkbox"
                                disabled={true}
                                name="status"
                                checked={task.status}
                            ></input>
                            <NavLink to={"#"}>{task.title}</NavLink>
                        </div>
                    ))}
                </nav>
            ) : null}
        </div>
    );
}
