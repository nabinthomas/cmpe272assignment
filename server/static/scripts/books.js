'use strict';

const element = React.createElement;

class BooksListHeadingRow extends React.Component {
    constructor(props) {
      super(props);
      this.state = { 
        headings : [
            "ISBN-13",
            "Title", 
            "Author(s)",
            "Price",
            "Available",
            "In Cart",
            "Add to Cart", // Add To Cart + button

        ]
      };
    }
    render() {
        let cells = [];

        for (var i = 0; i < this.state.headings.length; i++){
            cells.push(
                element('th', {key:i}, this.state.headings[i])
            );
        }
        return element(
            'tr',
            null,
            cells
        );
    }
}

class BookListData extends React.Component{
    constructor(props) {
        super(props);
        this.state = { 
          books : [
              {
                ISBN13: "1",
                Title: "The Jungle Book", 
                Author: "Rudyard Kipling",
                Price: 24.0,
                AvailableCopies: 399,
                InCartCopies:0
                // Add To Cart + button
              },
              {
                ISBN13: "12",
                Title: "The Jungle Book 2", 
                Author: "Rudyard Kipling",
                Price: 30.99,
                AvailableCopies: 9,
                InCartCopies:0
                // Add To Cart + button
              },
              {
                ISBN13: "123",
                Title: "The Adventures of Sherlock Holmes", 
                Author: "Sir Arthur Conan Doyle",
                Price: 22.97,
                AvailableCopies: 99,
                InCartCopies:0
                // Add To Cart + button
              }
          ]
        };
      }

      render() {
        let rows = [];
        for (var i = 0; i < this.state.books.length; i++){
            let cells = [];
            var isbn13id = `isbn13-${i}`;
            var titleId = `title-${i}`;
            var authorId= `author-${i}`;
            var priceId=`price-${i}`;
            var availableCopiesId = `copies-${i}`;
            var inCartCopiesId = `copies-${i}`;
            var addButtonId = `add-${i}`;
            var addButtonCellId = `add-button-cell-${i}`;
            cells.push(element('td', {key:isbn13id}, this.state.books[i].ISBN13));
            cells.push(element('td', {key:titleId}, this.state.books[i].Title));
            cells.push(element('td', {key:authorId}, this.state.books[i].Author));
            cells.push(element('td', {key:priceId, class:'price_cell'}, '$ ' + this.state.books[i].Price.toFixed(2)));
            cells.push(element('td', {key:availableCopiesId, class:'count_cell'}, this.state.books[i].AvailableCopies));
            cells.push(element('td', {key:inCartCopiesId, class:'count_cell'}, this.state.books[i].InCartCopies));
            var addButton = element('button', {key:addButtonId}, '+'); 
            cells.push(element('td', {key:addButtonCellId, class:'button_cell'}, addButton));
            var thisRow = element(
                'tr',
                {key:`book-${i}`},
                cells
            );
            // console.log(cells);
            rows.push(thisRow);
        }
        // console.log(rows);
        return rows;
    }
}

const book_list_heading = document.querySelector('#book_list_heading');
ReactDOM.render(element(BooksListHeadingRow), book_list_heading);
const book_list_data = document.querySelector('#book_list_data');
ReactDOM.render(element(BookListData), book_list_data);