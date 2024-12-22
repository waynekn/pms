import { camelCase, isArray, transform, isObject } from "lodash";

/**
 * Recursively transforms keys of an object from snake_case to camelCase.
 *
 * @param obj - Object to camelize.
 * @returns Object with keys transformed to camelCase.
 */
const camelize = (obj: Record<string, unknown>) =>
  transform(
    obj,
    (result: Record<string, unknown>, value: unknown, key: string, target) => {
      const camelKey = isArray(target) ? key : camelCase(key);
      result[camelKey] = isObject(value)
        ? camelize(value as Record<string, unknown>)
        : value;
    }
  );

export default camelize;
