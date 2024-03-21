import { Outlet } from "react-router-dom";
// import { NavLink, Form, useLoaderData } from "react-router-dom";
import { SideBar } from "./sidebar";

export default function Root() {
  return (
    <>
      <SideBar />
      <Outlet />
    </>
  );
}
