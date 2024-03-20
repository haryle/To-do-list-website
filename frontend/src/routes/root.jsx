import { Outlet } from "react-router-dom";
import { NavLink, Form, useLoaderData } from "react-router-dom";
import { getProjects, getTags } from "../data";


export async function loader() {
    const projects = await getProjects();
    const tags = await getTags();
    return { projects, tags }
}



function SideBar() {
    const { projects, tags } = useLoaderData();
    return (
        <div id="sidebar">
            {/* Title */}
            <NavLink to="/">
                <h1>Menu</h1>
            </NavLink>

            {/* Search Form */}
            <Form id="search-form" role="search">
                <input
                    type="search"
                    name="q"
                    placeholder="Find Project"
                />
                <div
                    id="search-spinner"
                    aria-hidden
                    hidden={true}
                />
            </Form>

            {/* Tasks */}
            <h2>Tasks</h2>
            <nav className="task_menu">
                <ul>
                    <NavLink className="upcoming" to="task/upcoming">Upcoming</NavLink>
                    <NavLink className="today" to="task/today">Today</NavLink>
                    <NavLink className="recent" to="task/most_recent">Recent</NavLink>
                    <NavLink className="incomplete" to="task/?status=false">Incomplete</NavLink>
                </ul>
            </nav>

            {/* Project */}
            <h2>Projects</h2>
            <nav className="project_menu">
                {projects.length &&
                    <ul>
                        {projects.map((project) => (
                            <NavLink key={project.id} to={`project/${project.id}`}>{project.title}</NavLink>
                        ))}
                    </ul>
                }
            </nav>

            {/* Tag */}
            <h2>Tags</h2>
            <nav className="tag_menu">
                {tags.length &&
                    <ul>
                        {tags.map((tag) => (
                            <NavLink key={tag.id} to={`tag/${tag.id}`}>{tag.title}</NavLink>
                        ))}
                    </ul>
                }
            </nav>
        </div>
    );
}




export default function Root() {
    return (
        <>
            <SideBar />
            <Outlet />
        </>
    )
}