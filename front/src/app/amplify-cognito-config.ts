"use client";
import { Amplify } from "aws-amplify";
import type { ResourcesConfig } from "aws-amplify";

const amplifyConfig: ResourcesConfig = {
  Auth: {
    Cognito: {
      userPoolId: process.env.NEXT_PUBLIC_USER_POOL_ID!,
      userPoolClientId: process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID!,
      region: process.env.NEXT_PUBLIC_COGNITO_REGION!,
    },
  },
};

Amplify.configure(amplifyConfig, { ssr: true });

export default function AmplifyCognitoConfig() {
  return null;
}
