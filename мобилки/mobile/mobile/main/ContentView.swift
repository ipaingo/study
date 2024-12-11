//
//  ContentView.swift
//  mobile
//
//  Created by Sofia on 29.10.2024.
//

import SwiftUI

struct ContentView: View {
    
    var body: some View {
        NavigationSplitView {
            List {
                NavigationLink {
                    Task1View()
                } label: {
                    Text("Задание 1")
                }
                NavigationLink {
                    Task2View()
                } label: {
                    Text("Задание 2")
                }
                NavigationLink {
                    Task3View()
                } label: {
                    Text("Задание 3")
                }
            }
            .navigationTitle("Меню")
        } detail: {
            Text("Проект по мобильной разработке на СвИфТе")
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        Task1View()
    }
}
