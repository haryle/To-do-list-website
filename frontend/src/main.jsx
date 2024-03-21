import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './index.css'
import Root from './routes/root';
import { 
  loaderProject, 
  loaderProjectId, 
  loaderDefaultProject, 
  actionCreateProject, 
  actionUpdateProject,
  actionDeleteProject
} from './routes/helper';
import ErrorPage from './error-page';
import ProjectPage from './routes/project';
import CreateProject from './routes/create';

const router = createBrowserRouter([
  {
    "path": "/",
    element: <Root/>,
    loader: loaderProject,
    errorElement: <ErrorPage/>,
    children: [
      {
        errorElement: <ErrorPage/>,
        children: [
          {
            "path": "/project/:projectId",
            element: <ProjectPage/>,
            loader: loaderProjectId
          },
          {
            "path": "/project/:projectId/delete",
            action: actionDeleteProject,
          },
          {
            "path": "/project/:projectId/update",
            action: actionUpdateProject,
          },
          {
            "path": "/project/default/create",
            element: <CreateProject />,
            loader: loaderDefaultProject,
            action: actionCreateProject,
          }
        ]
      }
    ]
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
)
