export type User = {
  pk: string;
  username: string;
  email: string;
  usernameSlug: string;
};

export type UserResponse = Omit<User, "usernameSlug"> & {
  username_slug: string;
};

export type CurrentUser = User & {
  isLoading: boolean;
  isLoggedIn: boolean;
};
