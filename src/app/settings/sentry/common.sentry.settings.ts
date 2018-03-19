export abstract class SentrySettingsInterface {
  public static readonly address: string;
  public static readonly port: number;
  public static readonly protocol: string;
  public static readonly token: string;

  public static getURL(): string {
    if (this.address && this.port && this.protocol && this.token) {
      return this.protocol + this.token + '@' + this.address + ':' + this.port + '/1';
    }
    return null;
  }
}

/**

  -----------------------
  USING SENTRY SETTINGS:
  -----------------------

    Create a class implementation in a file in this directory called local.sentry.settings.ts.
    An example configuration is below.

  -----------------------
  EXAMPLE CONFIGURATION:
  -----------------------

    import { SentrySettingsInterface } from './common.sentry.settings';

    export class SentrySettings extends SentrySettingsInterface {
      public static address: string = 'localhost';
      public static port: number = 9000;
      public static protocol: string = 'http://';
      public static token: string = '3d4bca0e8aa8465bae6fd29934f5ea0f';
    }

**/
