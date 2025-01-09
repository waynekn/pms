import { Routes, Route } from "react-router";

import HomePage from "./pages/home.page";
import LogInForm from "./components/login.component";
import LogoutPage from "./pages/logout.page";
import SignUpForm from "./components/signup.component";
import ProfilePage from "./pages/profle.page";
import ProjectDetailPage from "./pages/project-detail.page";
import ProjectPhasePage from "./pages/project-phases.page";
import ProjectPhaseDetail from "./pages/project-phase-detail.page";
import ProjectDashBoard from "./components/project-dashboard.component";
import ProjectMembersList from "./components/project-members-list.component";
import NonProjectMembersList from "./components/project-member-addition.component";
import ProjectTasksPage from "./pages/project-tasks.page";
import ProjectCreationPage from "./pages/project-create.page";
import OrganizationDetail from "./pages/organization-detail.page";
import GoogleCallback from "./components/google-callback.component";
import OrganizationCreationForm from "./pages/organization-creation.page";
import TemplateCreationForm from "./pages/template-creation.page";

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />}>
        <Route path="login/" element={<LogInForm />} />
        <Route path="signup/" element={<SignUpForm />} />
        <Route
          path="accounts/google/login/callback/"
          element={<GoogleCallback />}
        />
      </Route>
      <Route path="user/:username/" element={<ProfilePage />} />
      <Route path="logout/" element={<LogoutPage />} />
      <Route
        path="organization/create/"
        element={<OrganizationCreationForm />}
      />
      <Route
        path="organization/:organizationNameSlug/"
        element={<OrganizationDetail />}
      />
      <Route
        path=":organizationNameSlug/project/create"
        element={<ProjectCreationPage />}
      />
      <Route path="templates/create/" element={<TemplateCreationForm />} />
      <Route path="tasks/:projectId/" element={<ProjectTasksPage />} />
      <Route path="workflow/:projectId/" element={<ProjectPhasePage />} />
      <Route
        path="phase/:projectPhaseId/detail/"
        element={<ProjectPhaseDetail />}
      />
      <Route
        path=":projectId/:projectNameSlug/"
        element={<ProjectDetailPage />}
      >
        <Route index element={<ProjectDashBoard />} />
        <Route path="dashboard/" element={<ProjectDashBoard />} />
        <Route path="members/" element={<ProjectMembersList />} />
        <Route path="members/add/" element={<NonProjectMembersList />} />
      </Route>
    </Routes>
  );
};

export default Router;
