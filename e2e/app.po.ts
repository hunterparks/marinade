import { browser, by, element } from 'protractor';

export class AppPage {
  public getParagraphText(): any {
    return element(by.css('marinade-root h1')).getText();
  }

  public navigateTo(): any {
    return browser.get('/');
  }
}
