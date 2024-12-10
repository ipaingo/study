//
//  ContentView.swift
//  mobile
//
//  Created by Sofia on 29.10.2024.
//

import SwiftUI

struct ContentView: View {
    // @Binding var task4data: [Photo]
    // var loader: PhotoLoader
    
    var body: some View {
        NavigationSplitView {
            List {
                NavigationLink {
                    Task1View()
                } label: {
                    Text("Task 1")
                }
                NavigationLink {
                    Task2View()
                } label: {
                    Text("Task 2")
                }
                NavigationLink {
                    Task3View()
                } label: {
                    Text("Task 3")
                }
                NavigationLink {
                    Task4View()
                } label: {
                    Text("Task 4")
                }
            }
            .navigationTitle("Tasks")
        } detail: {
            Text("Mobile development project")
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        Task1View()
    }
}
