export type User = {
  pk: string;
  username: string;
  email: string;
  usernameSlug: string;
  profilePicture: string;
};

export type UserResponse = Omit<User, "usernameSlug" | "profilePicture"> & {
  username_slug: string;
  profile_picture: string;
};

export type CurrentUser = User & {
  isLoading: boolean;
  isLoggedIn: boolean;
};
