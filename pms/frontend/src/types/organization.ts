import { Project, ProjectResponse } from "./projects";

export type OrganizationMember = {
  username: string;
};

export type OrganizationResponse = {
  organization_id: string;
  organization_name: string;
  organization_name_slug: string;
};

export type Organization = {
  organizationId: string;
  organizationName: string;
  organizationNameSlug: string;
};

// Organization response from API.
export type OrganizationDetailResponse = {
  organization_id: string;
  organization_name: string;
  organization_name_slug: string;
  projects: ProjectResponse[];
  role: "Member" | "Admin";
};

// `OrganizationResponse` but with camel case keys
export type OrganziationDetail = {
  organizationId: string;
  organizationName: string;
  organizationNameSlug: string;
  role: "Member" | "Admin";
  projects: Project[];
};
