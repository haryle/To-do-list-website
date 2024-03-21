import { useLoaderData, NavLink, Form, Link } from "react-router-dom";

export function SideBar() {
  const projects = useLoaderData();
  return (
    <div id="sidebar">
      {/* Title */}
      <NavLink to="/">
        <h1>Menu</h1>
      </NavLink>

      {/* Search Form */}
      <Form id="search-form" role="search">
        <input type="search" name="q" placeholder="Find Project" />
        <div id="search-spinner" aria-hidden hidden={true} />
      </Form>

      {/* Tasks */}
      <span className="flexSpan">
        <h2>Tasks</h2>
        {/* <Button /> */}
      </span>
      <nav className="task_menu">
        <ul>
          <NavLink className="upcoming" to="task/upcoming">
            Upcoming
          </NavLink>
          <NavLink className="today" to="task/today">
            Today
          </NavLink>
          <NavLink className="recent" to="task/most_recent">
            Recent
          </NavLink>
          <NavLink className="incomplete" to="task/?status=false">
            Incomplete
          </NavLink>
        </ul>
      </nav>

      {/* Project */}
      <span className="flexSpan">
        <h2>Projects</h2>
        <Link to="project/default/create">+</Link>
      </span>

      {projects.length ? (
        <nav className="project_menu">
          {projects.map((project) => (
            <NavLink key={project.id} to={`project/${project.id}`}>
              {project.title}
            </NavLink>
          ))}
        </nav>
      ) : null}
    </div>
  );
}
