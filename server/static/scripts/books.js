'use strict';

const element = React.createElement;

class BooksListHeadingRow extends React.Component {
    constructor(props) {
      super(props);
      this.state = { 
        headings : [
            "Title", 
            "Author(s)",
            "Price",
            "Available",
            "", // Add To Cart + button

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
                Title: "The Jungle Book", 
                Author: "Rudyard Kipling",
                Price: 24,
                Copies: 399
                // Add To Cart + button
              },
              {
                Title: "The Jungle Book 2", 
                Author: "Rudyard Kipling",
                Price: 30,
                Copies: 9
                // Add To Cart + button
              },
              {
                Title: "The Adventures of Sherlock Holmes", 
                Author: "Sir Arthur Conan Doyle",
                Price: 22,
                Copies: 99
                // Add To Cart + button
              }
          ]
        };
      }

      render() {
        let cells = [];

        for (var i = 0; i < this.state.books.length; i++){
            var titleId = `cell${i}-title`;
            var authorId= `cell${i}-author`;
            var priceId=`cell${i}-price`;
            var copiesId = `cell${i}-copies`;
            cells.push(
                element(
                    'td', {key:titleId}, this.state.books[i].Title,
                    'td', {key:authorId}, this.state.books[i].Author,
                    'td', {key:priceId}, this.state.books[i].Price,
                    'td', {key:copiesId}, this.state.books[i].Copies
                    )
            );
        }
        return element(
            'tr',
            null,
            cells
        );
    }
}

const book_list_heading = document.querySelector('#book_list_heading');
ReactDOM.render(element(BooksListHeadingRow), book_list_heading);
const book_list_data = document.querySelector('#book_list_data');
ReactDOM.render(element(BookListData), book_list_data);