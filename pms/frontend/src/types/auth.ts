import { UserResponse } from "./user";

export type SuccessfulAuth = {
  user: UserResponse;
  access: string;
  refresh: string;
};

export type UnsuccessfulLogIn = {
  password?: string[];
  non_field_errors?: string[];
};

export type UnsuccessfulRegistration = {
  username?: string[];
  email?: string[];
  password1?: string[];
  password2?: string[];
  non_field_errors?: string[];
};

export type LogInCredentials = {
  username: string;
  password: string;
};

export type LogInFormErrors = {
  password?: string[];
  nonFieldErrors?: string[];
};

export type SignUpCredentials = {
  username: string;
  email: string;
  password1: string;
  password2: string;
};

export type SignUpFormErrors = {
  username?: string[];
  email?: string[];
  password1?: string[];
  nonFieldErrors?: string[];
};
