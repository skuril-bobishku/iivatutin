const isServer = typeof process !== 'undefined' && process.env;

function getEnvVariable(key, defaultValue) {
    const value = isServer ? process.env[key] : import.meta.env[key];
    if (!value) {
        console.warn(`Warning: Environment variable ${key} is not set. Using default: ${defaultValue}`);
        return defaultValue;
    }
    return value;
}

export function getUrl(key, defaultValue = 'localhost') {
    return getEnvVariable(key, defaultValue);
}

export function getPort(key, defaultValue = 5173) {
    const value = getEnvVariable(key, defaultValue);
    const port = parseInt(value, 10);
    if (isNaN(port)) {
        console.error(`Error: Environment variable ${key} is not a valid number. Using default: ${defaultValue}`);
        return defaultValue;
    }
    return port;
}