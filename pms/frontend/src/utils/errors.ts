import { AxiosError, isAxiosError } from "axios";

export type ErrorMessageConfig = {
  400?: string;
  403?: string;
  404?: string;
  500?: string;
};

type GenericApiError = {
  detail: string;
};

const handleGenericApiErrors = (
  error: unknown,
  messageConfig?: ErrorMessageConfig
): string => {
  if (isAxiosError(error)) {
    const statusCode = error.status;
    const axiosError = error as AxiosError<GenericApiError>;

    if (statusCode === 400) {
      return (
        axiosError.response?.data.detail ||
        messageConfig?.[400] ||
        "Bad request"
      );
    }

    if (statusCode === 403) {
      return (
        axiosError.response?.data.detail ||
        messageConfig?.[403] ||
        "You are not authorized to access this resource"
      );
    }

    if (statusCode === 404) {
      return (
        axiosError.response?.data.detail ||
        messageConfig?.[404] ||
        "Could not find the requested resource"
      );
    }

    if (!statusCode || statusCode >= 500) {
      return (
        axiosError.response?.data.detail ||
        messageConfig?.[500] ||
        "An unexpected error occurred"
      );
    }

    return "An unexpected error occurred";
  } else {
    return "An unexpected error occurred";
  }
};

export default handleGenericApiErrors;
