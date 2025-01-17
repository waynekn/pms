import { Industry, IndustryResponse } from "./industry";

export type TemplateSearchResponse = {
  template_id: string;
  template_name: string;
  industry: IndustryResponse;
};

export type ProjectTemplate = {
  templateId: string;
  templateName: string;
  industry: Industry;
};
