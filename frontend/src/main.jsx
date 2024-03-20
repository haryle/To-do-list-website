import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './index.css'
import Root, {loader as loaderRoot} from './routes/root';


const router = createBrowserRouter([
  {
    "path": "/",
    element: <Root/>,
    loader: loaderRoot,
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
)
