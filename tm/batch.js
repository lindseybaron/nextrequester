// ==UserScript==
// @name         nextrequester
// @namespace    nextrequest.com
// @version      0.1
// @description  make nextrequest usable
// @author       elbeh
// @match        https://*.nextrequest.com/requests/*
// @grant        none
// ==/UserScript==

(function() {
  'use strict';
  const HOST = document.location.origin;

  window.addEventListener('load', function() {

    let buttonStyle = [
      'background-color: rgb(255, 255, 255);' +
      'border: 2px solid #1c1c41;' +
      'border-radius: 4px; ' +
      'color: black;' +
      'padding: .25em;' +
      'text-align: center;' +
      'font-size: 100%;' +
      'font-weight: bolder;' +
      'margin-bottom: 5px;' +
      'margin-top: 5px;' +
      'cursor: pointer;',
    ].join(' ');
    let expBtn = document.createElement('div');
    let dlBtn = document.createElement('div');
    let links;

    expBtn.innerHTML = '<button style="' + buttonStyle + '">Expand Folders</button>';
    dlBtn.innerHTML = '<button style="' + buttonStyle + '">Grab Links</button>';

    expBtn.onclick = () => {
      expandAll();
      return false;
    };

    dlBtn.onclick = () => {
      links = grabAllDownloadLinks();
      return false;
    };

    document.querySelector("div.document-list > div.row").after(dlBtn);
    document.querySelector("div.document-list > div.row").after(expBtn);
  }, false);

  /*
    expand
  */

  function expandAll() {
    let docList = document.querySelector('.document-list');
    waitForLoaded();

    let closedToggles = docList.querySelectorAll('.fa-caret-right');
    console.log('Expanding ' + closedToggles.length + ' folders...');

    let thisClosed;
    for (let i = 0; i < closedToggles.length; i++) {
      thisClosed = closedToggles[i];
      thisClosed.click()
    }
  }

  /*
    links
  */

  function parseDownloadLinks(elements) {
    let data = [];
    for (let i = 0; i < elements.length; i++) {
      let elData = {
        'href': elements[i].getAttribute('href'),
        'filename': elements[i].textContent,
      };
      data.push(elData);
    }

    return data;
  }

  function grabVisibleLinks(el) {
    let links = el.querySelectorAll('.document-link');
    // console.log('> found ' + links.length + ' links.');

    return parseDownloadLinks(links);
  }

  function nextIsActive(nextLink) {
    let isActive = !nextLink.getAttribute('class').includes('disabled');
    console.log('NEXT IS ACTIVE: ' + isActive);
    console.log(nextLink.getAttribute('class'));

    return isActive;
  }

  function grabLinksFromFolder(folder) {
    let links = grabVisibleLinks(folder);
    // console.log('> check for NEXT link...');
    // if (folder.querySelector('.page.next')) {
    //   let next = folder.querySelector('.page.next');
    //   console.log('if the next link is active...');
    //   console.log('next link active: ' + !next.getAttribute('class').includes('disabled'))
    // while (!next.getAttribute('class').includes('disabled')) {
    //   console.log('click it...');
    //   next.querySelector('a').click();
    //   waitForLoaded();
    //   console.log('and grab the new links from the folder...');
    //   links.push(grabVisibleLinks(folder));
    // }
    // }

    return links;
  }

  function getLinksFromRows(rows) {
    let links = [];
    for (let i = 0; i < rows.length; i++) {
      if (!rows[i].getAttribute('class').includes('hide-for-print')) {
        let link = rows[i].querySelector('.document-link');
        let href = HOST + link.getAttribute('href');
        let filename = link.textContent;

        console.log([href, filename].join('\t'));
        if (href.length > 0 && filename.length > 0) {
          links.push({
            href: href,
            filename: filename,
          })
        }
      }
    }

    return links
  }

  function grabSectionLinks(section) {

    let links = [];

    // check the first page of the section
    console.log('Checking first page of section ' + section.getAttribute('id') + '...');
    let listPage = section.querySelector('.info-value');
    let rows = listPage.querySelectorAll('.row');

    // get the rows with just doc links
    let linkRows = [];
    for (let i = 0; i < rows.length; i++) {
      let rowClass = rows[i].getAttribute('class');
      if (!rowClass.includes('toggleable') && !rowClass.includes('hide-for-print')) {
        linkRows.push(rows[i]);
      }
    }
    console.log('linkRows: ' + linkRows.length);
    // SO FAR SO GOOD

    // get the non-folder links
    links.push(getLinksFromRows(linkRows));

    // get the rows that are collapsible folders
    let folders = listPage.querySelectorAll('.row.hide-for-print');
    console.log('folders: ' + folders.length);

    // get the folder links
    for (let i = 0; i < folders.length; i++) {
      let folderName = folders[i].querySelector('.font-size-14').textContent;
      console.log('Checking first page of folder ' + folderName);
      // check if expanded
      if (folders[i].querySelectorAll('.fa-caret-right').length > 0) {
        console.log('expand folder...');
        folders[i].querySelector('.fa-caret-right').click();
        waitForLoaded();
      }

      // check first page of folder
      let folderRows = folders[i].querySelectorAll('.row');
      let folderLinks = getLinksFromRows(folderRows);
      links.push(folderLinks);

      // check subsequent pages of folder
      if (folders[i].querySelectorAll('.pagy-nav').length > 0) {
        // get pagination
        let pagy =  folders[i].querySelector('.pagy-nav');
        let pageNumbers = getPagination(pagy);
        // iterate over pages
      }
    }

    let navSelector = '#' + section.getAttribute('id') + ' > nav';
    let pageNumbers;

    if (document.querySelectorAll(navSelector).length > 0) {
      let pagy = document.querySelector(navSelector);
      pageNumbers = getPagination(pagy);
      console.log('Found ' + pageNumbers.length + ' pages in section ' + section.getAttribute('id') + '.');

      for (let i = 2; i > pageNumbers.length; i++) {
        console.log('Navigating to page ' + pageNumbers[i].textContent
            + ' in section ' + section.getAttribute('id') + '...');
        goToPage(i);
      }
    }

  return links;

  //   console.log('1. grab all currently visible links in section ' + section.getAttribute('id') + '...');
  //   let links = grabVisibleLinks(section);
  //
  //   console.log('2. check for hidden folders in section ' + section.getAttribute('id') + '...');
  //   if (section.querySelectorAll('.row.hide-for-print')) {
  //     console.log('3. grab all the hidden folders in section ' + section.getAttribute('id') + '...');
  //     let folders = section.querySelectorAll('div.row.hide-for-print');
  //     console.log('4. iterate over ' + folders.length + ' folders in section ' + section.getAttribute('id') + '...');
  //     for (let i = 0; i < folders; i++) {
  //       links.push(grabLinksFromFolder(folders[i]));
  //     }
  //   }
  //
  //   console.log('5. check for additional pages in section ' + section.getAttribute('id') + '...');
  //   navSelector = '#' + section.getAttribute('id') + ' > nav';
  //
  //   console.log('6. if there is a pagination nav...');
  //   if (document.querySelectorAll(navSelector).length > 0) {
  //
  //     console.log('7. get all the page numbers in section ' + section.getAttribute('id') + '...');
  //     let pageNumbers = document.querySelector(navSelector).querySelectorAll('.page');
  //     let activePage = document.querySelector(navSelector).querySelectorAll('.page.active').textContent;
  //
  //     for (let i = 2; i < pageNumbers.length - 2; i++) {
  //       console.log('i: ' + i);
  //       console.log('activePage: ' + activePage);
  //       console.log('totalPages: ' + pageNumbers.length - 2);
  //
  //       console.log('8. click the next page...');
  //       document.querySelector(navSelector).querySelectorAll('.page')[i].querySelector('a').click();
  //       waitForLoaded();
  //
  //       console.log('9. and grab the new links from the document list...');
  //       links.push(grabVisibleLinks(section));
  //
  //       console.log('10. check for hidden folders in section ' + section.getAttribute('id') + '...');
  //       if (section.querySelectorAll('.row.hide-for-print')) {
  //         console.log('11. grab all the hidden folders...');
  //         let folders = section.querySelectorAll('div.row.hide-for-print');
  //
  //         console.log('12. iterate over the ' + folders.length + ' folders...');
  //         for (let i = 0; i < folders; i++) {
  //           links.push(grabLinksFromFolder(folders[i]));
  //         }
  //       }
  //     }
  //   } else {
  //     console.log('no page nav found in section ' + section.getAttribute('id') + '...');
  //   }
  //
  //   console.log('found ' + links.length + ' links in section ' + section.getAttribute('id'));
  //   return links;
  }

  function grabAllDownloadLinks() {
    waitForLoaded();

    let sections = document.querySelectorAll('.js-doc-box > div');
    let links = [];

    for (let i = 0; i < sections.length; i++) {
      links.push(grabSectionLinks(sections[i]));
    }

    console.log(links.toString())
  }

  /*
    pagination
  */

  function getPagination(pageNav) {
    let pageLinks = pageNav.querySelectorAll('.page');
    let pages = [];
    for (let i = 0; i < pageLinks.length; i++) {
      if (!pageLinks[i].getAttribute('class').includes('prev')
          && !pageLinks[i].getAttribute('class').includes('next')) {
        pages.push(pageLinks[i]);
      }
    }

    return pages;
  }

  function goToPage(pagy, pageNumber) {
    let pages = getPagination(pagy);
    let page = pages[pageNumber - 1].querySelector('a');
    page.click();
    waitForLoaded();
  }

  /*
    common
  */

  function waitForLoaded() {
    let docList = document.querySelector('.document-list');
    if(document.querySelectorAll('.vex-loading-spinner').length > 0 || docList.textContent.includes("loading")) {
      console.log('loading...');
      window.setTimeout(waitForLoaded, 1000);
    }
  }
})();