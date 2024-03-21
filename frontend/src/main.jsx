import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './index.css'
import Root from './routes/root';
import { loaderProject } from './routes/helper';
import ErrorPage from './error-page';
import ProjectPage from './routes/project';

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
